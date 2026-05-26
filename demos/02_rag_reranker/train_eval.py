from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import choose_device, ensure_dir, hashed_char_ngrams, mean_reciprocal_rank, save_json, set_seed, top1_accuracy


TRAIN_QUERIES = [
    ("private local inference", ["Local models keep sensitive text on the laptop.", "A recipe explains sourdough hydration.", "Football tables list wins and draws."]),
    ("local privacy", ["Running local inference keeps private data on the machine.", "Pasta water should be salted before noodles.", "Slide decks often have speaker notes."]),
    ("adapter training", ["LoRA updates small adapter matrices instead of every base weight.", "Museum opening hours change on holidays.", "A tokenizer maps text to ids."]),
    ("LoRA fine tuning", ["LoRA fine tuning adapts a model with small trainable matrices.", "Calendar invites include dates and times.", "Final workshops contain short talks."]),
    ("model card", ["A model card records risks, intended use, and evaluation limits.", "Apples can be stored in a cool pantry.", "A terminal command starts a server."]),
    ("verifiable rewards", ["A verifier can score exact answers or unit tests automatically.", "Long context increases KV cache memory.", "Students submit a PDF report."]),
    ("automatic reward", ["Automatic verifiers compute rewards from correct structured answers.", "Routers can choose tool calls.", "Long documents may contain tables."]),
    ("reranker", ["A reranker scores query document pairs after retrieval.", "A weather forecast predicts rain.", "A spreadsheet cell can contain a formula."]),
]

TEST_QUERIES = [
    ("local privacy", ["Running locally can avoid sending private data to an API.", "A slide deck has speaker notes.", "Pasta water should be salted."]),
    ("LoRA fine tuning", ["LoRA adapter training is a parameter efficient fine tuning method.", "The final workshop has short talks.", "A calendar invite has a start time."]),
    ("automatic reward", ["A verifiable reward checks whether generated output is correct.", "A long document may contain tables.", "A router chooses a tool call."]),
]


class Reranker(nn.Module):
    def __init__(self, dim: int):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(dim * 4 + 3, 128), nn.ReLU(), nn.Linear(128, 1))

    def forward(self, query: torch.Tensor, doc: torch.Tensor) -> torch.Tensor:
        dot = (query * doc).sum(dim=-1, keepdim=True)
        q_norm = query.norm(p=2, dim=-1, keepdim=True)
        d_norm = doc.norm(p=2, dim=-1, keepdim=True)
        features = torch.cat([query, doc, query * doc, (query - doc).abs(), dot, q_norm, d_norm], dim=-1)
        return self.net(features).squeeze(-1)


def make_pairs(rows: list[tuple[str, list[str]]]) -> list[tuple[str, str, int]]:
    pairs = []
    for query, docs in rows:
        for idx, doc in enumerate(docs):
            pairs.append((query, doc, int(idx == 0)))
    return pairs


@torch.no_grad()
def evaluate(model: Reranker, rows: list[tuple[str, list[str]]], device: torch.device) -> dict:
    rankings = []
    for query, docs in rows:
        q = hashed_char_ngrams(query).to(device)
        query_rows = []
        for idx, doc in enumerate(docs):
            d = hashed_char_ngrams(doc).to(device)
            score = torch.sigmoid(model(q[None, :], d[None, :]))[0].item()
            query_rows.append((doc, score, int(idx == 0)))
        rankings.append(query_rows)
    return {
        "mrr": mean_reciprocal_rank(rankings),
        "top1_accuracy": top1_accuracy(rankings),
        "rankings": [
            {
                "query": query,
                "docs": [
                    {"doc": doc, "score": score, "relevant": bool(label)}
                    for doc, score, label in sorted(rows_for_query, key=lambda item: item[1], reverse=True)
                ],
            }
            for (query, _), rows_for_query in zip(rows, rankings)
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=320)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--out", default="outputs/demos/02_rag_reranker")
    args = parser.parse_args()

    set_seed(103)
    device = choose_device(args.device)
    train_pairs = make_pairs(TRAIN_QUERIES)
    q = torch.stack([hashed_char_ngrams(query) for query, _, _ in train_pairs]).to(device)
    d = torch.stack([hashed_char_ngrams(doc) for _, doc, _ in train_pairs]).to(device)
    y = torch.tensor([label for _, _, label in train_pairs], dtype=torch.float32, device=device)
    model = Reranker(q.size(-1)).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3)
    initial = evaluate(model, TEST_QUERIES, device)

    for step in range(1, args.steps + 1):
        logits = model(q, d)
        loss = F.binary_cross_entropy_with_logits(logits, y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if step == 1 or step % 80 == 0:
            acc = ((torch.sigmoid(logits) > 0.5).float() == y).float().mean().item()
            print(f"step {step:04d} loss {loss.item():.4f} train_pair_acc {acc:.3f}")

    final = evaluate(model, TEST_QUERIES, device)
    summary = {
        "demo": "rag_reranker",
        "device": str(device),
        "steps": args.steps,
        "initial_eval": initial,
        "final_eval": final,
        "mrr_delta": final["mrr"] - initial["mrr"],
        "top1_delta": final["top1_accuracy"] - initial["top1_accuracy"],
    }
    out = ensure_dir(args.out)
    torch.save({"model": model.state_dict()}, out / "checkpoint.pt")
    save_json(out / "summary.json", summary)
    print(summary)


if __name__ == "__main__":
    main()
