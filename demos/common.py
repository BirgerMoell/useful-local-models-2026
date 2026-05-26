from __future__ import annotations

import json
import math
import random
import string
import zlib
from pathlib import Path

import torch


TEXT_ALPHABET = string.ascii_lowercase + string.digits + " -_:/.,{}[]()\"'\n"


def set_seed(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)


def choose_device(name: str = "auto") -> torch.device:
    if name != "auto":
        return torch.device(name)
    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def ensure_dir(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_json(path: str | Path, data: dict) -> None:
    path = Path(path)
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def hashed_char_ngrams(text: str, dim: int = 384, n_min: int = 2, n_max: int = 4) -> torch.Tensor:
    text = " " + text.lower() + " "
    vec = torch.zeros(dim, dtype=torch.float32)
    for n in range(n_min, n_max + 1):
        if len(text) < n:
            continue
        for i in range(len(text) - n + 1):
            gram = text[i : i + n]
            vec[zlib.crc32(gram.encode("utf-8")) % dim] += 1.0
    return vec / (vec.norm(p=2) + 1e-6)


def accuracy(pred: list[str], gold: list[str]) -> float:
    if not gold:
        return 0.0
    return sum(p == g for p, g in zip(pred, gold)) / len(gold)


def mean_reciprocal_rank(rankings: list[list[tuple[str, float, int]]]) -> float:
    scores = []
    for docs in rankings:
        sorted_docs = sorted(docs, key=lambda item: item[1], reverse=True)
        rank = next((idx + 1 for idx, (_, _, label) in enumerate(sorted_docs) if label == 1), None)
        scores.append(0.0 if rank is None else 1.0 / rank)
    return sum(scores) / len(scores)


def top1_accuracy(rankings: list[list[tuple[str, float, int]]]) -> float:
    hits = 0
    for docs in rankings:
        best = max(docs, key=lambda item: item[1])
        hits += int(best[2] == 1)
    return hits / len(rankings)


def bits_per_token(loss_nats: float) -> float:
    return loss_nats / math.log(2)
