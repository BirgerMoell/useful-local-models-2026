from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch

sys.path.append(str(Path(__file__).resolve().parents[1]))
from tiny_models import CharTokenizer, TinyCausalLM, cross_entropy_loss, ensure_dir, make_lm_batch, save_json, set_seed


def build_corpus() -> str:
    docs = []
    for i in range(80):
        key = chr(ord("a") + (i % 8))
        filler = " ".join([f"detail{i % 5}" for _ in range(10)])
        docs.append(f"document {i}: key {key}. {filler}. answer {key}.\n")
    return "".join(docs)


@torch.no_grad()
def eval_loss(model: TinyCausalLM, ids: list[int], seq_len: int, rope_scale: float, device: torch.device) -> float:
    model.eval()
    losses = []
    for _ in range(10):
        x, y = make_lm_batch(ids, batch_size=8, seq_len=seq_len, device=device)
        losses.append(cross_entropy_loss(model(x, rope_scale=rope_scale), y).item())
    model.train()
    return sum(losses) / len(losses)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=240)
    parser.add_argument("--short-len", type=int, default=48)
    parser.add_argument("--long-len", type=int, default=128)
    parser.add_argument("--rope-scale", type=float, default=4.0)
    parser.add_argument("--out", default="outputs/05_context_extension")
    args = parser.parse_args()

    set_seed(19)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    corpus = build_corpus()
    tokenizer = CharTokenizer([corpus])
    ids = tokenizer.encode(corpus * 20, add_bos=True, add_eos=True)
    config = {"dim": 96, "heads": 4, "layers": 2}
    model = TinyCausalLM(tokenizer.vocab_size, **config).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=2e-3)

    short_steps = args.steps // 2
    for step in range(1, args.steps + 1):
        seq_len = args.short_len if step <= short_steps else args.long_len
        rope_scale = 1.0 if step <= short_steps else args.rope_scale
        x, y = make_lm_batch(ids, batch_size=8, seq_len=seq_len, device=device)
        loss = cross_entropy_loss(model(x, rope_scale=rope_scale), y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if step == 1 or step == short_steps or step % 60 == 0:
            phase = "short" if step <= short_steps else "long"
            print(f"step {step:04d} phase {phase} loss {loss.item():.4f}")

    short_loss = eval_loss(model, ids, args.short_len, 1.0, device)
    long_loss_unscaled = eval_loss(model, ids, args.long_len, 1.0, device)
    long_loss_scaled = eval_loss(model, ids, args.long_len, args.rope_scale, device)

    summary = {
        "short_loss": short_loss,
        "long_loss_unscaled_rope": long_loss_unscaled,
        "long_loss_scaled_rope": long_loss_scaled,
        "note": "Cheap context-extension evidence is only a measurement, not a capability claim.",
    }
    out = ensure_dir(args.out)
    torch.save({"model": model.state_dict(), "vocab": tokenizer.itos, "config": config, "summary": summary}, out / "checkpoint.pt")
    save_json(out / "summary.json", summary)
    print(summary)


if __name__ == "__main__":
    main()
