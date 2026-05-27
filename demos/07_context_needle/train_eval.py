from __future__ import annotations

import argparse
import random
import re
import sys
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import choose_device, ensure_dir, save_json, set_seed


VALUES = ["red", "blue", "green", "amber", "silver", "violet", "cyan", "white"]
VALUE_TO_ID = {value: idx for idx, value in enumerate(VALUES)}


class NeedleReader(nn.Module):
    def __init__(self, slots: int, values: int, dim: int = 48):
        super().__init__()
        self.slot_keys = nn.Parameter(torch.randn(slots, dim) * 0.02)
        self.query = nn.Linear(slots, dim, bias=False)
        self.out = nn.Linear(values, values)

    def forward(self, slot_values: torch.Tensor, target_slot: torch.Tensor) -> torch.Tensor:
        query = self.query(target_slot)
        attn = torch.softmax(query @ self.slot_keys.T, dim=-1)
        selected = torch.bmm(attn[:, None, :], slot_values).squeeze(1)
        return self.out(selected)


def make_record(rng: random.Random, slots: int) -> tuple[str, int, int, str]:
    values = [rng.choice(VALUES) for _ in range(slots)]
    target = rng.randrange(slots)
    facts = " | ".join(f"s{i:02d}={value}" for i, value in enumerate(values))
    text = f"question: value of s{target:02d}?\nfacts: {facts}\nanswer:"
    return text, target, VALUE_TO_ID[values[target]], values[target]


def parse_record(text: str, slots: int) -> tuple[torch.Tensor, torch.Tensor]:
    target_match = re.search(r"value of s(\d+)\?", text)
    if target_match is None:
        raise ValueError(f"Missing target slot in: {text}")
    target_idx = int(target_match.group(1))
    slot_values = torch.zeros(slots, len(VALUES), dtype=torch.float32)
    for slot, value in re.findall(r"s(\d+)=(red|blue|green|amber|silver|violet|cyan|white)", text):
        slot_idx = int(slot)
        if 0 <= slot_idx < slots:
            slot_values[slot_idx, VALUE_TO_ID[value]] = 1.0
    target = torch.zeros(slots, dtype=torch.float32)
    target[target_idx] = 1.0
    return slot_values, target


def make_batch(rng: random.Random, batch_size: int, slots: int, device: torch.device) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    records = [make_record(rng, slots) for _ in range(batch_size)]
    parsed = [parse_record(text, slots) for text, _, _, _ in records]
    slot_values = torch.stack([item[0] for item in parsed]).to(device)
    target_slots = torch.stack([item[1] for item in parsed]).to(device)
    labels = torch.tensor([label for _, _, label, _ in records], dtype=torch.long, device=device)
    return slot_values, target_slots, labels


@torch.no_grad()
def evaluate(model: NeedleReader, rows: list[tuple[str, int, int, str]], slots: int, device: torch.device) -> dict:
    model.eval()
    parsed = [parse_record(text, slots) for text, _, _, _ in rows]
    slot_values = torch.stack([item[0] for item in parsed]).to(device)
    target_slots = torch.stack([item[1] for item in parsed]).to(device)
    labels = torch.tensor([label for _, _, label, _ in rows], dtype=torch.long, device=device)
    pred = model(slot_values, target_slots).argmax(dim=-1)
    examples = []
    for text, _, label, value, guess in zip((r[0] for r in rows[:10]), (r[1] for r in rows[:10]), labels[:10].tolist(), (r[3] for r in rows[:10]), pred[:10].tolist()):
        examples.append(
            {
                "prompt": text[:220],
                "gold": value,
                "pred": VALUES[guess],
                "correct": guess == label,
            }
        )
    model.train()
    return {"exact_accuracy": (pred == labels).float().mean().item(), "examples": examples}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=260)
    parser.add_argument("--slots", type=int, default=18)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--out", default="outputs/demos/07_context_needle")
    args = parser.parse_args()

    set_seed(108)
    device = choose_device(args.device)
    train_rng = random.Random(108)
    eval_rows = [make_record(random.Random(9000 + i), args.slots) for i in range(160)]
    model = NeedleReader(args.slots, len(VALUES)).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3)
    initial = evaluate(model, eval_rows, args.slots, device)

    for step in range(1, args.steps + 1):
        slot_values, target_slots, labels = make_batch(train_rng, args.batch_size, args.slots, device)
        logits = model(slot_values, target_slots)
        loss = F.cross_entropy(logits, labels)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if step == 1 or step % 65 == 0:
            acc = (logits.argmax(dim=-1) == labels).float().mean().item()
            print(f"step {step:04d} loss {loss.item():.4f} train_acc {acc:.3f}")

    final = evaluate(model, eval_rows, args.slots, device)
    summary = {
        "demo": "context_needle",
        "data": "synthetic long-record key/value retrieval with known answers",
        "device": str(device),
        "steps": args.steps,
        "slots_per_record": args.slots,
        "initial_eval": initial,
        "final_eval": final,
        "exact_accuracy_delta": final["exact_accuracy"] - initial["exact_accuracy"],
        "note": "Records are parsed into slot/value features; the trained attention reader learns which slot to select.",
    }
    out = ensure_dir(args.out)
    torch.save({"model": model.state_dict(), "values": VALUES, "slots": args.slots}, out / "checkpoint.pt")
    save_json(out / "summary.json", summary)
    print(summary)


if __name__ == "__main__":
    main()
