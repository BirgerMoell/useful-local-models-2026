from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch

sys.path.append(str(Path(__file__).resolve().parents[1]))
from tiny_models import CharTokenizer, TinyCausalLM, cross_entropy_loss, ensure_dir, make_lm_batch, save_json, set_seed


PAIRS = [
    ("classify: this was helpful", "positive"),
    ("classify: this saved time", "positive"),
    ("classify: this failed badly", "negative"),
    ("classify: this was confusing", "negative"),
    ("rewrite: use local models", "local models should run on your machine"),
    ("rewrite: compare to baseline", "compare the trained system to a simple baseline"),
]


def format_example(prompt: str, answer: str) -> str:
    return f"Instruction: {prompt}\nAnswer: {answer}\n\n"


@torch.no_grad()
def answer(model: TinyCausalLM, tokenizer: CharTokenizer, prompt: str, device: torch.device) -> str:
    prefix = f"Instruction: {prompt}\nAnswer:"
    ids = torch.tensor([tokenizer.encode(prefix, add_bos=True)], device=device)
    out = model.generate(ids, max_new_tokens=48, eos_id=tokenizer.eos_id, temperature=0.0)
    text = tokenizer.decode(out[0].tolist())
    return text.split("Answer:", 1)[-1].strip().splitlines()[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=300)
    parser.add_argument("--out", default="outputs/02_instruction_tuning")
    args = parser.parse_args()

    set_seed(11)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    texts = [format_example(p, a) for p, a in PAIRS]
    tokenizer = CharTokenizer(texts)
    token_ids = tokenizer.encode("".join(texts) * 150, add_bos=True, add_eos=True)
    config = {"dim": 112, "heads": 4, "layers": 2}
    model = TinyCausalLM(tokenizer.vocab_size, **config).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=2e-3)

    for step in range(1, args.steps + 1):
        x, y = make_lm_batch(token_ids, batch_size=16, seq_len=64, device=device)
        loss = cross_entropy_loss(model(x), y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if step == 1 or step % 75 == 0:
            print(f"step {step:04d} loss {loss.item():.4f}")

    probes = ["classify: this was helpful", "classify: this failed badly", "rewrite: compare to baseline"]
    predictions = {probe: answer(model, tokenizer, probe, device) for probe in probes}
    out = ensure_dir(args.out)
    torch.save({"model": model.state_dict(), "vocab": tokenizer.itos, "config": config, "predictions": predictions}, out / "checkpoint.pt")
    save_json(out / "summary.json", {"final_loss": float(loss.item()), "predictions": predictions})
    print("\nPredictions:")
    for probe, pred in predictions.items():
        print(f"- {probe} -> {pred}")


if __name__ == "__main__":
    main()
