from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import accuracy, choose_device, ensure_dir, hashed_char_ngrams, save_json, set_seed


TRAIN = [
    ("find papers about LoRA adapters", "search"),
    ("search for context extension papers", "search"),
    ("look up Qwen local deployment", "search"),
    ("run the held out evaluation", "evaluate"),
    ("score the test split", "evaluate"),
    ("measure json validity", "evaluate"),
    ("train a small instruction adapter", "train"),
    ("start the reranker training run", "train"),
    ("fine tune the local model", "train"),
    ("train a tool calling model", "train"),
    ("fine tune tool call behavior", "train"),
    ("export a gguf model", "export"),
    ("make an ollama package", "export"),
    ("convert the adapter for local inference", "export"),
    ("open the model card", "inspect"),
    ("read the dataset card", "inspect"),
    ("show the artifact manifest", "inspect"),
    ("inspect the eval config", "inspect"),
    ("show the training configuration", "inspect"),
    ("open train yaml", "inspect"),
]

TEST = [
    ("search recent GRPO examples", "search"),
    ("evaluate the validation split", "evaluate"),
    ("train the tool calling model", "train"),
    ("export for llama cpp", "export"),
    ("inspect the training config", "inspect"),
]


LABELS = ["evaluate", "export", "inspect", "search", "train"]
TOOL_CALLS = {
    "evaluate": {"tool": "evaluate", "args": {"split": "test"}},
    "export": {"tool": "export", "args": {"format": "gguf"}},
    "inspect": {"tool": "read_file", "args": {"path": "artifact_manifest.yaml"}},
    "search": {"tool": "search", "args": {"query": "<query>"}},
    "train": {"tool": "train", "args": {"method": "sft_lora"}},
}


class Router(nn.Module):
    def __init__(self, dim: int, labels: int):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(dim, 96), nn.ReLU(), nn.Linear(96, labels))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


@torch.no_grad()
def evaluate(model: Router, rows: list[tuple[str, str]], device: torch.device) -> dict:
    x = torch.stack([hashed_char_ngrams(text) for text, _ in rows]).to(device)
    logits = model(x)
    pred_ids = logits.argmax(dim=-1).cpu().tolist()
    pred = [LABELS[i] for i in pred_ids]
    gold = [label for _, label in rows]
    calls = [TOOL_CALLS[label] for label in pred]
    valid_json = 0
    for call in calls:
        json.loads(json.dumps(call))
        valid_json += 1
    return {
        "accuracy": accuracy(pred, gold),
        "valid_json_rate": valid_json / len(rows),
        "predictions": [
            {"input": text, "gold": label, "pred": guess, "tool_call": TOOL_CALLS[guess]}
            for (text, label), guess in zip(rows, pred)
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=260)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--out", default="outputs/demos/01_tool_router")
    args = parser.parse_args()

    set_seed(102)
    device = choose_device(args.device)
    train_x = torch.stack([hashed_char_ngrams(text) for text, _ in TRAIN]).to(device)
    train_y = torch.tensor([LABELS.index(label) for _, label in TRAIN], device=device)
    model = Router(train_x.size(-1), len(LABELS)).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=4e-3)
    initial = evaluate(model, TEST, device)

    for step in range(1, args.steps + 1):
        logits = model(train_x)
        loss = F.cross_entropy(logits, train_y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if step == 1 or step % 65 == 0:
            train_acc = (logits.argmax(dim=-1) == train_y).float().mean().item()
            print(f"step {step:04d} loss {loss.item():.4f} train_acc {train_acc:.3f}")

    final = evaluate(model, TEST, device)
    summary = {
        "demo": "tool_router",
        "device": str(device),
        "steps": args.steps,
        "initial_eval": initial,
        "final_eval": final,
        "accuracy_delta": final["accuracy"] - initial["accuracy"],
    }
    out = ensure_dir(args.out)
    torch.save({"model": model.state_dict(), "labels": LABELS}, out / "checkpoint.pt")
    save_json(out / "summary.json", summary)
    print(summary)


if __name__ == "__main__":
    main()
