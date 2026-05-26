from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch

sys.path.append(str(Path(__file__).resolve().parents[1]))
from tiny_models import CharTokenizer, TinyCausalLM, cross_entropy_loss, ensure_dir, make_lm_batch, save_json, set_seed


EXAMPLES = [
    ("search papers about LoRA", '{"tool":"search","args":{"query":"LoRA"}}'),
    ("run evaluation on test set", '{"tool":"evaluate","args":{"split":"test"}}'),
    ("summarize model card", '{"tool":"read_file","args":{"path":"cards/model_card.md"}}'),
    ("train instruction adapter", '{"tool":"train","args":{"method":"sft_lora"}}'),
    ("export for local runtime", '{"tool":"export","args":{"format":"gguf"}}'),
]


def format_example(user: str, call: str) -> str:
    return f"User: {user}\nAssistant tool_call: {call}\n\n"


@torch.no_grad()
def complete(model: TinyCausalLM, tokenizer: CharTokenizer, user: str, device: torch.device) -> str:
    prefix = f"User: {user}\nAssistant tool_call:"
    ids = torch.tensor([tokenizer.encode(prefix, add_bos=True)], device=device)
    out = model.generate(ids, max_new_tokens=90, eos_id=tokenizer.eos_id, temperature=0.0)
    text = tokenizer.decode(out[0].tolist())
    return text.split("Assistant tool_call:", 1)[-1].strip().splitlines()[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=260)
    parser.add_argument("--out", default="outputs/06_tool_use_sft")
    args = parser.parse_args()

    set_seed(23)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    texts = [format_example(u, c) for u, c in EXAMPLES]
    tokenizer = CharTokenizer(texts)
    ids = tokenizer.encode("".join(texts) * 120, add_bos=True, add_eos=True)
    config = {"dim": 112, "heads": 4, "layers": 2}
    model = TinyCausalLM(tokenizer.vocab_size, **config).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=2e-3)

    for step in range(1, args.steps + 1):
        x, y = make_lm_batch(ids, batch_size=16, seq_len=96, device=device)
        loss = cross_entropy_loss(model(x), y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if step == 1 or step % 65 == 0:
            print(f"step {step:04d} loss {loss.item():.4f}")

    probes = ["run evaluation on test set", "export for local runtime"]
    predictions = {probe: complete(model, tokenizer, probe, device) for probe in probes}
    out = ensure_dir(args.out)
    torch.save({"model": model.state_dict(), "vocab": tokenizer.itos, "config": config, "predictions": predictions}, out / "checkpoint.pt")
    save_json(out / "summary.json", {"final_loss": float(loss.item()), "predictions": predictions})
    print(predictions)


if __name__ == "__main__":
    main()

