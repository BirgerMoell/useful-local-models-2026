from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch

sys.path.append(str(Path(__file__).resolve().parents[2] / "examples"))
sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import bits_per_token, choose_device, ensure_dir, save_json, set_seed
from tiny_models import CharTokenizer, TinyCausalLM, cross_entropy_loss, make_lm_batch


CORPUS = [
    "A useful local model has a narrow task, a measured baseline, and a runnable artifact.\n",
    "Training only counts when model parameters are updated and the change is evaluated.\n",
    "A model card records the intended use, limitations, risks, and local runtime.\n",
    "Small models can be useful when the output format is constrained and the data is private.\n",
    "The evaluation split must stay separate from the training corpus.\n",
    "Long context claims need tasks where the answer depends on far-away evidence.\n",
    "A reranker scores query document pairs and can improve local retrieval without text generation.\n",
    "Verifiable rewards work best when a program can check whether an answer is correct.\n",
    "Agent assistance is useful only when diffs, prompts, and decisions stay auditable.\n",
    "Gemma and Qwen style small models are realistic adapter targets on local hardware.\n",
]


@torch.no_grad()
def eval_loss(model: TinyCausalLM, ids: list[int], seq_len: int, device: torch.device) -> float:
    model.eval()
    losses = []
    repeated = ids * max(2, (seq_len * 16) // max(1, len(ids)))
    for _ in range(12):
        x, y = make_lm_batch(repeated, batch_size=8, seq_len=seq_len, device=device)
        losses.append(cross_entropy_loss(model(x), y).item())
    model.train()
    return sum(losses) / len(losses)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=320)
    parser.add_argument("--seq-len", type=int, default=96)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--out", default="outputs/demos/00_next_token_lm")
    args = parser.parse_args()

    set_seed(101)
    device = choose_device(args.device)
    train_texts = CORPUS[:8]
    eval_texts = CORPUS[8:]
    tokenizer = CharTokenizer(CORPUS)
    train_ids = tokenizer.encode("".join(train_texts) * 80, add_bos=True, add_eos=True)
    eval_ids = tokenizer.encode("".join(eval_texts) * 80, add_bos=True, add_eos=True)
    config = {"dim": 128, "heads": 4, "layers": 2}
    model = TinyCausalLM(tokenizer.vocab_size, **config).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=2e-3)

    initial_eval_loss = eval_loss(model, eval_ids, args.seq_len, device)
    for step in range(1, args.steps + 1):
        x, y = make_lm_batch(train_ids, args.batch_size, args.seq_len, device)
        loss = cross_entropy_loss(model(x), y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if step == 1 or step % 80 == 0:
            print(f"step {step:04d} train_loss {loss.item():.4f}")

    final_train_loss = eval_loss(model, train_ids, args.seq_len, device)
    final_eval_loss = eval_loss(model, eval_ids, args.seq_len, device)
    prompt = "A useful local model"
    ids = torch.tensor([tokenizer.encode(prompt, add_bos=True)], device=device)
    generated = model.generate(ids, max_new_tokens=120, eos_id=tokenizer.eos_id, temperature=0.7)
    sample = tokenizer.decode(generated[0].tolist())

    summary = {
        "demo": "next_token_lm",
        "device": str(device),
        "steps": args.steps,
        "initial_eval_loss": initial_eval_loss,
        "initial_eval_bits_per_token": bits_per_token(initial_eval_loss),
        "final_train_loss": final_train_loss,
        "final_eval_loss": final_eval_loss,
        "final_eval_bits_per_token": bits_per_token(final_eval_loss),
        "eval_loss_delta": initial_eval_loss - final_eval_loss,
        "sample": sample,
    }
    out = ensure_dir(args.out)
    torch.save({"model": model.state_dict(), "vocab": tokenizer.itos, "config": config}, out / "checkpoint.pt")
    save_json(out / "summary.json", summary)
    print(summary)


if __name__ == "__main__":
    main()
