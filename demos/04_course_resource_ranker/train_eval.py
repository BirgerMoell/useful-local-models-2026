from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import choose_device, ensure_dir, hashed_char_ngrams, mean_reciprocal_rank, save_json, set_seed, top1_accuracy


DOC_PATHS = [
    "student-project-brief.md",
    "project-tracks.md",
    "project-format.md",
    "training-pipeline-spec.md",
    "local-deployment-guide.md",
    "model-menu-and-compute.md",
    "advanced-techniques-guide.md",
    "modern-tooling-map.md",
    "rubric.md",
    "milestones-and-schedule.md",
    "teacher-overview.md",
    "teacher-start-checklist.md",
    "assignment-pages/studium-proposal-assignment.md",
    "assignment-pages/studium-progress-seminars.md",
    "assignment-pages/studium-final-report.md",
    "templates/model-card-template.md",
    "templates/dataset-card-template.md",
    "templates/experiment-log-template.md",
]


DOC_HINTS = {
    "student-project-brief.md": "student brief final artifact local artifact project deliverables",
    "project-tracks.md": "tracks choose choosing instruction tuning rag reranking rlvr grpo context multilingual projects",
    "project-format.md": "format structure project flow question evidence training release",
    "training-pipeline-spec.md": "pipeline data baseline train evaluate release training steps",
    "local-deployment-guide.md": "local inference deploy deployment publish package artifact gguf ollama mlx llama cpp",
    "model-menu-and-compute.md": "model menu compute qwen qwen3.5 gemma gemma4 laptop memory realistic",
    "advanced-techniques-guide.md": "advanced grpo rlvr dpo context extension rewards techniques",
    "modern-tooling-map.md": "agents tooling modern ai assistants prompts diffs experiments",
    "rubric.md": "rubric graded evaluated claim metrics usefulness evidence",
    "milestones-and-schedule.md": "schedule deadlines milestones proposals progress seminars dates",
    "teacher-overview.md": "teacher overview run course theme",
    "teacher-start-checklist.md": "teacher checklist prepare before course starts",
    "assignment-pages/studium-proposal-assignment.md": "proposal assignment studium research plan abstract slides",
    "assignment-pages/studium-progress-seminars.md": "progress seminars studium report update blockers",
    "assignment-pages/studium-final-report.md": "final report studium paper submission artifact",
    "templates/model-card-template.md": "model card intended use limitations risks metrics",
    "templates/dataset-card-template.md": "dataset card source license split privacy",
    "templates/experiment-log-template.md": "experiment log failed run decision hypothesis metric summary",
}


TRAIN_QUERIES = [
    ("What should the final artifact include?", "student-project-brief.md"),
    ("Which track covers DPO and preference tuning?", "project-tracks.md"),
    ("How should students structure the project work?", "project-format.md"),
    ("What belongs in the training pipeline?", "training-pipeline-spec.md"),
    ("How do I package a model for local inference?", "local-deployment-guide.md"),
    ("Which Gemma or Qwen model should a laptop group try?", "model-menu-and-compute.md"),
    ("Where are GRPO and context extension explained?", "advanced-techniques-guide.md"),
    ("How can students use agents and modern tooling?", "modern-tooling-map.md"),
    ("How will projects be graded?", "rubric.md"),
    ("When are proposals and progress seminars due?", "milestones-and-schedule.md"),
    ("What should teachers prepare before the course starts?", "teacher-start-checklist.md"),
    ("What should the proposal assignment say in Studium?", "assignment-pages/studium-proposal-assignment.md"),
    ("How do progress seminars work?", "assignment-pages/studium-progress-seminars.md"),
    ("What should the final report ask students to submit?", "assignment-pages/studium-final-report.md"),
    ("What fields should a model card contain?", "templates/model-card-template.md"),
    ("What goes into a dataset card?", "templates/dataset-card-template.md"),
    ("How should an experiment run be logged?", "templates/experiment-log-template.md"),
    ("Students choose among instruction tuning, RAG, RLVR, and context extension tracks.", "project-tracks.md"),
    ("A group asks whether Gemma 4 or Qwen3.5 fits on a laptop.", "model-menu-and-compute.md"),
    ("Publish a model so another student can run it locally.", "local-deployment-guide.md"),
    ("Grade whether the project made a useful local model.", "rubric.md"),
    ("Find the proposal text for Studium.", "assignment-pages/studium-proposal-assignment.md"),
    ("Record a failed run, metric movement, and next decision.", "templates/experiment-log-template.md"),
]


TEST_QUERIES = [
    ("Project tracks for instruction tuning, RAG reranking, DPO, RLVR, and context extension.", "project-tracks.md"),
    ("Model menu compute note for Qwen3.5 0.8B and Gemma 4 E2B laptop runs.", "model-menu-and-compute.md"),
    ("Local deployment guide for publishing a GGUF, Ollama, or MLX artifact.", "local-deployment-guide.md"),
    ("Rubric for grading usefulness evidence, metrics, errors, and baseline comparison.", "rubric.md"),
    ("Studium proposal assignment text with research plan, abstract, and slides.", "assignment-pages/studium-proposal-assignment.md"),
    ("Experiment log template for a failed run, metric movement, and next decision.", "templates/experiment-log-template.md"),
]


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "be",
    "before",
    "can",
    "do",
    "for",
    "how",
    "i",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "should",
    "the",
    "to",
    "what",
    "where",
    "with",
}


class ResourceRanker(nn.Module):
    def __init__(self, dim: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim, 48),
            nn.ReLU(),
            nn.Dropout(0.05),
            nn.Linear(48, 1),
        )

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return self.net(features).squeeze(-1)


def clean_markdown(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[#>*_\-|]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_corpus(root: Path) -> dict[str, str]:
    corpus = {}
    for rel in DOC_PATHS:
        raw = (root / rel).read_text(encoding="utf-8")
        title = next((line.lstrip("# ").strip() for line in raw.splitlines() if line.startswith("#")), rel)
        corpus[rel] = f"{rel}\n{title}\n{DOC_HINTS.get(rel, '')}\n{clean_markdown(raw)[:2600]}"
    return corpus


def words(text: str) -> set[str]:
    return {word for word in re.findall(r"[a-z0-9.]+", text.lower()) if word not in STOPWORDS and len(word) > 1}


def pair_features(query: str, rel: str, doc: str) -> torch.Tensor:
    q_words = words(query)
    d_words = words(doc)
    path_words = words(rel.replace("/", " ").replace("-", " ").replace("_", " ").replace(".", " "))
    overlap = q_words & d_words
    path_overlap = q_words & path_words
    q_vec = hashed_char_ngrams(query, dim=384)
    d_vec = hashed_char_ngrams(doc, dim=384)
    cosine = float((q_vec * d_vec).sum().item())
    return torch.tensor(
        [
            cosine,
            len(overlap) / max(1, len(q_words | d_words)),
            len(overlap) / max(1, len(q_words)),
            len(path_overlap) / max(1, len(q_words)),
            len(path_overlap),
            1.0 if any(word in rel.lower() for word in q_words) else 0.0,
            len(q_words),
        ],
        dtype=torch.float32,
    )


def build_training_pairs(corpus: dict[str, str]) -> list[tuple[str, str, str, int]]:
    pairs = []
    for query, gold_path in TRAIN_QUERIES:
        for rel, doc in corpus.items():
            pairs.append((query, rel, doc, int(rel == gold_path)))
    return pairs


@torch.no_grad()
def evaluate(model: ResourceRanker, corpus: dict[str, str], queries: list[tuple[str, str]], device: torch.device) -> dict:
    rankings = []
    display = []
    for query, gold_path in queries:
        rows = []
        for rel, doc in corpus.items():
            features = pair_features(query, rel, doc).to(device)
            score = torch.sigmoid(model(features[None, :]))[0].item()
            rows.append((rel, score, int(rel == gold_path)))
        rows.sort(key=lambda item: item[1], reverse=True)
        rankings.append(rows)
        display.append(
            {
                "query": query,
                "gold": gold_path,
                "top3": [{"path": rel, "score": round(score, 4), "relevant": bool(label)} for rel, score, label in rows[:3]],
            }
        )
    return {
        "mrr": mean_reciprocal_rank(rankings),
        "top1_accuracy": top1_accuracy(rankings),
        "rankings": display,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=260)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--out", default="outputs/demos/04_course_resource_ranker")
    args = parser.parse_args()

    set_seed(105)
    device = choose_device(args.device)
    root = Path(__file__).resolve().parents[2]
    corpus = load_corpus(root)
    pairs = build_training_pairs(corpus)
    features = torch.stack([pair_features(query, rel, doc) for query, rel, doc, _ in pairs]).to(device)
    labels = torch.tensor([label for _, _, _, label in pairs], dtype=torch.float32, device=device)
    model = ResourceRanker(features.size(-1)).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3, weight_decay=0.01)
    pos_weight = torch.tensor([(labels == 0).sum().item() / max(1, (labels == 1).sum().item())], device=device)
    initial = evaluate(model, corpus, TEST_QUERIES, device)

    for step in range(1, args.steps + 1):
        logits = model(features)
        loss = F.binary_cross_entropy_with_logits(logits, labels, pos_weight=pos_weight)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if step == 1 or step % 65 == 0:
            pair_acc = ((torch.sigmoid(logits) > 0.5).float() == labels).float().mean().item()
            print(f"step {step:04d} loss {loss.item():.4f} train_pair_acc {pair_acc:.3f}")

    final = evaluate(model, corpus, TEST_QUERIES, device)
    summary = {
        "demo": "course_resource_ranker",
        "data": "real repository Markdown course resources plus query labels",
        "device": str(device),
        "steps": args.steps,
        "documents": len(corpus),
        "train_queries": len(TRAIN_QUERIES),
        "test_queries": len(TEST_QUERIES),
        "initial_eval": initial,
        "final_eval": final,
        "mrr_delta": final["mrr"] - initial["mrr"],
        "top1_delta": final["top1_accuracy"] - initial["top1_accuracy"],
    }
    out = ensure_dir(args.out)
    torch.save({"model": model.state_dict(), "doc_paths": DOC_PATHS}, out / "checkpoint.pt")
    save_json(out / "summary.json", summary)
    print(summary)


if __name__ == "__main__":
    main()
