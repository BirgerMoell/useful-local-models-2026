from __future__ import annotations

import json
import random
from pathlib import Path

import torch
import torch.nn.functional as F


def set_seed(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)


def ensure_dir(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_json(path: str | Path, data: dict) -> None:
    path = Path(path)
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def make_lm_batch(
    ids: list[int],
    batch_size: int,
    seq_len: int,
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor]:
    max_start = len(ids) - seq_len - 1
    if max_start <= 0:
        raise ValueError("Need more tokens than seq_len for a language-model batch.")
    starts = torch.randint(0, max_start, (batch_size,))
    x = torch.stack([torch.tensor(ids[s : s + seq_len]) for s in starts])
    y = torch.stack([torch.tensor(ids[s + 1 : s + seq_len + 1]) for s in starts])
    return x.to(device), y.to(device)


def cross_entropy_loss(logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
    return F.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))

