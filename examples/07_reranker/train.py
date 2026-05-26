from __future__ import annotations

import argparse
import string
import sys
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.append(str(Path(__file__).resolve().parents[1]))
from tiny_models import ensure_dir, save_json, set_seed


PAIRS = [
    ("local model privacy", "local models keep sensitive data on the machine", 1),
    ("local model privacy", "football results and league tables", 0),
    ("instruction tuning", "supervised fine tuning teaches prompt answer behavior", 1),
    ("instruction tuning", "a recipe for sourdough bread", 0),
    ("verifiable rewards", "unit tests can score code completions automatically", 1),
    ("verifiable rewards", "a museum opening hour page", 0),
    ("context extension", "long context must be evaluated by evidence position", 1),
    ("context extension", "short poem about a city", 0),
]


VOCAB = {ch: i + 1 for i, ch in enumerate(string.ascii_lowercase + " ")}


def featurize(text: str) -> torch.Tensor:
    vec = torch.zeros(len(VOCAB) + 1)
    for ch in text.lower():
        vec[VOCAB.get(ch, 0)] += 1
    return vec / (vec.sum() + 1e-6)


class TinyReranker(nn.Module):
    def __init__(self, dim: int):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(dim * 3, 64), nn.ReLU(), nn.Linear(64, 1))

    def forward(self, query: torch.Tensor, doc: torch.Tensor) -> torch.Tensor:
        features = torch.cat([query, doc, query * doc], dim=-1)
        return self.net(features).squeeze(-1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=200)
    parser.add_argument("--out", default="outputs/07_reranker")
    args = parser.parse_args()

    set_seed(29)
    q = torch.stack([featurize(query) for query, _, _ in PAIRS])
    d = torch.stack([featurize(doc) for _, doc, _ in PAIRS])
    y = torch.tensor([label for _, _, label in PAIRS], dtype=torch.float32)
    model = TinyReranker(q.size(-1))
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3)

    for step in range(1, args.steps + 1):
        logits = model(q, d)
        loss = F.binary_cross_entropy_with_logits(logits, y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if step == 1 or step % 50 == 0:
            acc = ((torch.sigmoid(logits) > 0.5).float() == y).float().mean().item()
            print(f"step {step:04d} loss {loss.item():.4f} acc {acc:.3f}")

    with torch.no_grad():
        scores = torch.sigmoid(model(q, d)).tolist()
    summary = {
        "scores": [
            {"query": query, "doc": doc, "label": label, "score": score}
            for (query, doc, label), score in zip(PAIRS, scores)
        ]
    }
    out = ensure_dir(args.out)
    torch.save({"model": model.state_dict(), "vocab": VOCAB, "summary": summary}, out / "checkpoint.pt")
    save_json(out / "summary.json", summary)
    print("Saved reranker summary.")


if __name__ == "__main__":
    main()

