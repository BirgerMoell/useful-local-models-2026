from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path

import torch
import torch.nn.functional as F

sys.path.append(str(Path(__file__).resolve().parents[1]))
from tiny_models import CharTokenizer, TinyCausalLM, ensure_dir, save_json, set_seed


PREFS = [
    ("Question: What should a model card say?\nAnswer:", " limits and evals.", " it is amazing."),
    ("Question: What is a useful local model?\nAnswer:", " one that beats a baseline.", " a very large API."),
    ("Question: What should we report?\nAnswer:", " data, metric, and runtime.", " only a nice demo."),
    ("Question: Why use a baseline?\nAnswer:", " to test whether training helped.", " because it sounds formal."),
]


def logprob_completion(model: TinyCausalLM, tokenizer: CharTokenizer, prompt: str, completion: str, device: torch.device) -> torch.Tensor:
    prompt_ids = tokenizer.encode(prompt, add_bos=True)
    completion_ids = tokenizer.encode(completion, add_eos=True)
    ids = torch.tensor([prompt_ids + completion_ids], device=device)
    logits = model(ids[:, :-1])
    targets = ids[:, 1:]
    logp = F.log_softmax(logits, dim=-1)
    token_logp = logp.gather(-1, targets.unsqueeze(-1)).squeeze(-1)
    start = max(0, len(prompt_ids) - 1)
    return token_logp[:, start:].sum()


@torch.no_grad()
def generate_answer(model: TinyCausalLM, tokenizer: CharTokenizer, prompt: str, device: torch.device) -> str:
    ids = torch.tensor([tokenizer.encode(prompt, add_bos=True)], device=device)
    out = model.generate(ids, max_new_tokens=42, eos_id=tokenizer.eos_id, temperature=0.0)
    return tokenizer.decode(out[0].tolist())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=160)
    parser.add_argument("--beta", type=float, default=0.1)
    parser.add_argument("--out", default="outputs/03_preference_dpo")
    args = parser.parse_args()

    set_seed(13)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    texts = [p + w + l for p, w, l in PREFS]
    tokenizer = CharTokenizer(texts)
    config = {"dim": 96, "heads": 4, "layers": 2}
    policy = TinyCausalLM(tokenizer.vocab_size, **config).to(device)
    reference = copy.deepcopy(policy).to(device).eval()
    for p in reference.parameters():
        p.requires_grad_(False)
    opt = torch.optim.AdamW(policy.parameters(), lr=1e-3)

    for step in range(1, args.steps + 1):
        prompt, chosen, rejected = PREFS[(step - 1) % len(PREFS)]
        pi_chosen = logprob_completion(policy, tokenizer, prompt, chosen, device)
        pi_rejected = logprob_completion(policy, tokenizer, prompt, rejected, device)
        with torch.no_grad():
            ref_chosen = logprob_completion(reference, tokenizer, prompt, chosen, device)
            ref_rejected = logprob_completion(reference, tokenizer, prompt, rejected, device)
        margin = args.beta * ((pi_chosen - pi_rejected) - (ref_chosen - ref_rejected))
        loss = -F.logsigmoid(margin)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if step == 1 or step % 40 == 0:
            print(f"step {step:04d} dpo_loss {loss.item():.4f} margin {margin.item():.4f}")

    probe = "Question: What should we report?\nAnswer:"
    sample = generate_answer(policy, tokenizer, probe, device)
    out = ensure_dir(args.out)
    torch.save({"model": policy.state_dict(), "vocab": tokenizer.itos, "config": config, "sample": sample}, out / "checkpoint.pt")
    save_json(out / "summary.json", {"final_loss": float(loss.item()), "sample": sample})
    print("\nSample:")
    print(sample)


if __name__ == "__main__":
    main()
