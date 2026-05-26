from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import choose_device, ensure_dir, save_json, set_seed


MAX_ANSWER = 18
FEATURE_DIM = 10 + 10 + 19 + 1


def features(a: int, b: int) -> torch.Tensor:
    x = torch.zeros(FEATURE_DIM, dtype=torch.float32)
    x[a] = 1.0
    x[10 + b] = 1.0
    x[20 + a + b] = 1.0
    x[-1] = 1.0
    return x


class Policy(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(FEATURE_DIM, 64), nn.Tanh(), nn.Linear(64, MAX_ANSWER + 1))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def reward(answer: int, gold: int) -> float:
    if answer == gold:
        return 1.0
    distance = abs(answer - gold)
    return max(-0.2, 0.25 - 0.08 * distance)


@torch.no_grad()
def evaluate(policy: Policy, device: torch.device) -> dict:
    rows = []
    correct = 0
    for a in range(10):
        for b in range(10):
            x = features(a, b).to(device)
            pred = int(policy(x).argmax().item())
            gold = a + b
            correct += int(pred == gold)
            if len(rows) < 12:
                rows.append({"prompt": f"{a}+{b}=", "gold": gold, "pred": pred, "reward": reward(pred, gold)})
    return {"exact_accuracy": correct / 100, "samples": rows}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=360)
    parser.add_argument("--group-size", type=int, default=24)
    parser.add_argument("--sampled-group", action="store_true")
    parser.add_argument("--objective", choices=["verifier-ce", "group-policy"], default="verifier-ce")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--out", default="outputs/demos/03_rlvr_arithmetic")
    args = parser.parse_args()

    set_seed(104)
    device = choose_device(args.device)
    policy = Policy().to(device)
    opt = torch.optim.AdamW(policy.parameters(), lr=5e-3)
    initial = evaluate(policy, device)

    for step in range(1, args.steps + 1):
        a = ((step - 1) // 10) % 10
        b = (step - 1) % 10
        gold = a + b
        x = features(a, b).to(device)
        logits = policy(x)
        probs = torch.softmax(logits, dim=-1)
        logprobs_all = torch.log_softmax(logits, dim=-1)
        all_actions = torch.arange(MAX_ANSWER + 1, device=device)
        all_rewards = torch.tensor([reward(int(action), gold) for action in all_actions], dtype=torch.float32, device=device)
        if args.objective == "verifier-ce":
            target = int(all_rewards.argmax().item())
            loss = F.cross_entropy(logits[None, :], torch.tensor([target], device=device))
            rewards = all_rewards
        else:
            if args.sampled_group:
                actions = torch.multinomial(probs, num_samples=args.group_size, replacement=True)
                logprobs = logprobs_all[actions]
                rewards = torch.tensor([reward(int(action), gold) for action in actions], dtype=torch.float32, device=device)
                weights = torch.ones_like(rewards) / len(rewards)
            else:
                logprobs = logprobs_all
                rewards = all_rewards
                weights = probs.detach()
            advantages = (rewards - rewards.mean()) / (rewards.std(unbiased=False) + 1e-6)
            loss = -(weights * logprobs * advantages.detach()).sum()
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if step == 1 or step % 180 == 0:
            greedy = int(policy(x).argmax().item())
            print(f"step {step:04d} prompt {a}+{b}= gold {gold} greedy {greedy} reward_mean {rewards.mean().item():.3f}")

    final = evaluate(policy, device)
    summary = {
        "demo": "rlvr_arithmetic",
        "device": str(device),
        "steps": args.steps,
        "group_size": args.group_size,
        "sampled_group": args.sampled_group,
        "objective": args.objective,
        "initial_eval": initial,
        "final_eval": final,
        "exact_accuracy_delta": final["exact_accuracy"] - initial["exact_accuracy"],
        "note": "The reward is computed by a deterministic verifier; no labeled completion dataset is stored.",
    }
    out = ensure_dir(args.out)
    torch.save({"model": policy.state_dict()}, out / "checkpoint.pt")
    save_json(out / "summary.json", summary)
    print(summary)


if __name__ == "__main__":
    main()
