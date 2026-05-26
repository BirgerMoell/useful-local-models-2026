from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch

sys.path.append(str(Path(__file__).resolve().parents[1]))
from tiny_models import CharTokenizer, TinyCausalLM, cross_entropy_loss, ensure_dir, make_lm_batch, save_json, set_seed


TEXTS = [
    "small models can be useful when the task is narrow.\n",
    "local models protect data and make experiments inspectable.\n",
    "a baseline tells us whether training helped.\n",
    "evaluation turns a demo into evidence.\n",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=200)
    parser.add_argument("--seq-len", type=int, default=48)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--out", default="outputs/01_pretraining")
    args = parser.parse_args()

    set_seed(7)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = CharTokenizer(TEXTS)
    token_ids = tokenizer.encode("".join(TEXTS) * 120, add_bos=True, add_eos=True)
    config = {"dim": 96, "heads": 4, "layers": 2}
    model = TinyCausalLM(tokenizer.vocab_size, **config).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3)

    for step in range(1, args.steps + 1):
        x, y = make_lm_batch(token_ids, args.batch_size, args.seq_len, device)
        logits = model(x)
        loss = cross_entropy_loss(logits, y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if step == 1 or step % 50 == 0:
            print(f"step {step:04d} loss {loss.item():.4f}")

    prompt = "local models"
    input_ids = torch.tensor([tokenizer.encode(prompt, add_bos=True)], device=device)
    generated = model.generate(input_ids, max_new_tokens=80, eos_id=tokenizer.eos_id, temperature=0.7)
    sample = tokenizer.decode(generated[0].tolist())

    out = ensure_dir(args.out)
    torch.save(
        {"model": model.state_dict(), "vocab": tokenizer.itos, "config": config, "sample": sample},
        out / "checkpoint.pt",
    )
    save_json(out / "summary.json", {"final_loss": float(loss.item()), "sample": sample})
    print("\nSample:")
    print(sample)


if __name__ == "__main__":
    main()
