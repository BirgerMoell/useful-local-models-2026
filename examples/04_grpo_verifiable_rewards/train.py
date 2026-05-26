from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch
import torch.nn.functional as F

sys.path.append(str(Path(__file__).resolve().parents[1]))
from tiny_models import CharTokenizer, TinyCausalLM, ensure_dir, save_json, set_seed


PROBLEMS = [(1, 1), (1, 2), (2, 2), (2, 3), (3, 3), (4, 2)]


def prompt(a: int, b: int) -> str:
    return f"{a}+{b}="


def reward_fn(completion: str, gold: int) -> float:
    answer = completion.strip()[:1]
    if not answer.isdigit():
        return -0.2
    return 1.0 if int(answer) == gold else 0.0


def sample_completion(model: TinyCausalLM, tokenizer: CharTokenizer, text: str, device: torch.device) -> tuple[str, torch.Tensor]:
    ids = torch.tensor([tokenizer.encode(text, add_bos=True)], device=device)
    logits = model(ids)[:, -1, :]
    probs = torch.softmax(logits, dim=-1)
    next_id = torch.multinomial(probs, num_samples=1)
    logprob = torch.log(probs.gather(-1, next_id).squeeze(-1) + 1e-8).sum()
    return tokenizer.decode(next_id[0].tolist()), logprob


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--group-size", type=int, default=6)
    parser.add_argument("--out", default="outputs/04_grpo_verifiable_rewards")
    args = parser.parse_args()

    set_seed(17)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    all_text = "".join(prompt(a, b) + str(a + b) + "\n" for a, b in PROBLEMS)
    tokenizer = CharTokenizer([all_text])
    config = {"dim": 96, "heads": 4, "layers": 2}
    model = TinyCausalLM(tokenizer.vocab_size, **config).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=2e-3)

    for step in range(1, args.steps + 1):
        a, b = PROBLEMS[(step - 1) % len(PROBLEMS)]
        gold = a + b
        logprobs = []
        rewards = []
        completions = []
        for _ in range(args.group_size):
            completion, logprob = sample_completion(model, tokenizer, prompt(a, b), device)
            logprobs.append(logprob)
            rewards.append(reward_fn(completion, gold))
            completions.append(completion)
        reward_tensor = torch.tensor(rewards, device=device)
        advantages = (reward_tensor - reward_tensor.mean()) / (reward_tensor.std(unbiased=False) + 1e-6)
        loss = -(torch.stack(logprobs) * advantages.detach()).mean()
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if step == 1 or step % 20 == 0:
            print(f"step {step:04d} reward_mean {reward_tensor.mean().item():.3f} loss {loss.item():.4f}")

    eval_rewards = []
    samples = {}
    for a, b in PROBLEMS:
        completion, _ = sample_completion(model, tokenizer, prompt(a, b), device)
        samples[prompt(a, b)] = completion
        eval_rewards.append(reward_fn(completion, a + b))
    out = ensure_dir(args.out)
    torch.save({"model": model.state_dict(), "vocab": tokenizer.itos, "config": config, "samples": samples}, out / "checkpoint.pt")
    save_json(out / "summary.json", {"mean_reward": sum(eval_rewards) / len(eval_rewards), "samples": samples})
    print("\nSamples:")
    for p, c in samples.items():
        print(f"- {p}{c}")


if __name__ == "__main__":
    main()
