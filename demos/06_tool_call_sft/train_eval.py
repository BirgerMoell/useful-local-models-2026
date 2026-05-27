from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import choose_device, ensure_dir, hashed_char_ngrams, save_json, set_seed


TRAIN = [
    ("find papers about LoRA adapters", {"tool": "search", "args": {"query": "papers about LoRA adapters"}}),
    ("search for context extension evaluation", {"tool": "search", "args": {"query": "context extension evaluation"}}),
    ("look up local Qwen deployment", {"tool": "search", "args": {"query": "local Qwen deployment"}}),
    ("search GRPO papers", {"tool": "search", "args": {"query": "GRPO papers"}}),
    ("train the instruction adapter", {"tool": "train", "args": {"method": "sft_lora"}}),
    ("fine tune the tool calling model", {"tool": "train", "args": {"method": "tool_sft"}}),
    ("start reranker training", {"tool": "train", "args": {"method": "reranker"}}),
    ("train a document ranker", {"tool": "train", "args": {"method": "reranker"}}),
    ("evaluate the validation split", {"tool": "evaluate", "args": {"split": "validation"}}),
    ("score held out JSON validity", {"tool": "evaluate", "args": {"split": "json_validity"}}),
    ("run final test metrics", {"tool": "evaluate", "args": {"split": "test"}}),
    ("evaluate the test run", {"tool": "evaluate", "args": {"split": "test"}}),
    ("export the model to gguf", {"tool": "export", "args": {"format": "gguf"}}),
    ("make an ollama package", {"tool": "export", "args": {"format": "ollama"}}),
    ("convert adapter for local inference", {"tool": "export", "args": {"format": "adapter"}}),
    ("export with llama cpp", {"tool": "export", "args": {"format": "gguf"}}),
    ("open the model card", {"tool": "inspect", "args": {"path": "model-card.md"}}),
    ("read the dataset card", {"tool": "inspect", "args": {"path": "dataset-card.md"}}),
    ("show the experiment log", {"tool": "inspect", "args": {"path": "summary.json"}}),
    ("inspect the manifest file", {"tool": "inspect", "args": {"path": "artifact_manifest.yaml"}}),
]


TEST = [
    ("search recent GRPO examples", {"tool": "search", "args": {"query": "recent GRPO examples"}}),
    ("train the course resource ranker", {"tool": "train", "args": {"method": "reranker"}}),
    ("evaluate the test split", {"tool": "evaluate", "args": {"split": "test"}}),
    ("export for llama cpp", {"tool": "export", "args": {"format": "gguf"}}),
    ("inspect the artifact manifest", {"tool": "inspect", "args": {"path": "artifact_manifest.yaml"}}),
]


TOOLS = ["search", "train", "evaluate", "export", "inspect"]
METHODS = ["none", "sft_lora", "tool_sft", "reranker"]
SPLITS = ["none", "validation", "json_validity", "test"]
FORMATS = ["none", "gguf", "ollama", "adapter"]
PATHS = ["none", "model-card.md", "dataset-card.md", "summary.json", "artifact_manifest.yaml"]


class ToolCaller(nn.Module):
    def __init__(self, dim: int):
        super().__init__()
        self.trunk = nn.Sequential(nn.Linear(dim, 128), nn.ReLU(), nn.Linear(128, 96), nn.ReLU())
        self.tool = nn.Linear(96, len(TOOLS))
        self.method = nn.Linear(96, len(METHODS))
        self.split = nn.Linear(96, len(SPLITS))
        self.format = nn.Linear(96, len(FORMATS))
        self.path = nn.Linear(96, len(PATHS))

    def forward(self, x: torch.Tensor) -> dict[str, torch.Tensor]:
        h = self.trunk(x)
        return {
            "tool": self.tool(h),
            "method": self.method(h),
            "split": self.split(h),
            "format": self.format(h),
            "path": self.path(h),
        }


def canonical_query(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^(find|search|look up)\s+(for\s+)?", "", text, flags=re.I)
    return text.strip()


def labels_for(call: dict) -> dict[str, int]:
    args = call["args"]
    return {
        "tool": TOOLS.index(call["tool"]),
        "method": METHODS.index(args.get("method", "none")),
        "split": SPLITS.index(args.get("split", "none")),
        "format": FORMATS.index(args.get("format", "none")),
        "path": PATHS.index(args.get("path", "none")),
    }


def render_call(text: str, pred: dict[str, int]) -> dict:
    tool = TOOLS[pred["tool"]]
    if tool == "search":
        return {"tool": "search", "args": {"query": canonical_query(text)}}
    if tool == "train":
        if "rank" in text.lower():
            method = "reranker"
        elif "tool" in text.lower():
            method = "tool_sft"
        else:
            method = METHODS[pred["method"]] if pred["method"] else "sft_lora"
        return {"tool": "train", "args": {"method": method}}
    if tool == "evaluate":
        return {"tool": "evaluate", "args": {"split": SPLITS[pred["split"]] if pred["split"] else "validation"}}
    if tool == "export":
        return {"tool": "export", "args": {"format": FORMATS[pred["format"]] if pred["format"] else "gguf"}}
    return {"tool": "inspect", "args": {"path": PATHS[pred["path"]] if pred["path"] else "artifact_manifest.yaml"}}


def loss_for(outputs: dict[str, torch.Tensor], labels: dict[str, torch.Tensor]) -> torch.Tensor:
    return sum(F.cross_entropy(outputs[name], labels[name]) for name in labels)


@torch.no_grad()
def evaluate(model: ToolCaller, rows: list[tuple[str, dict]], device: torch.device) -> dict:
    model.eval()
    x = torch.stack([hashed_char_ngrams(text) for text, _ in rows]).to(device)
    outputs = model(x)
    pred_ids = {name: logits.argmax(dim=-1).cpu().tolist() for name, logits in outputs.items()}
    examples = []
    tool_hits = 0
    exact_hits = 0
    valid_json = 0
    for idx, (text, gold) in enumerate(rows):
        pred = {name: values[idx] for name, values in pred_ids.items()}
        call = render_call(text, pred)
        json.loads(json.dumps(call))
        valid_json += 1
        tool_hits += int(call["tool"] == gold["tool"])
        exact_hits += int(call == gold)
        examples.append({"input": text, "gold": gold, "prediction": call})
    model.train()
    return {
        "tool_accuracy": tool_hits / len(rows),
        "exact_call_accuracy": exact_hits / len(rows),
        "json_valid_rate": valid_json / len(rows),
        "examples": examples,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=220)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--out", default="outputs/demos/06_tool_call_sft")
    args = parser.parse_args()

    set_seed(107)
    device = choose_device(args.device)
    train_x = torch.stack([hashed_char_ngrams(text) for text, _ in TRAIN]).to(device)
    label_rows = [labels_for(call) for _, call in TRAIN]
    train_y = {
        name: torch.tensor([row[name] for row in label_rows], dtype=torch.long, device=device)
        for name in ["tool", "method", "split", "format", "path"]
    }
    model = ToolCaller(train_x.size(-1)).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3, weight_decay=0.01)
    initial = evaluate(model, TEST, device)

    for step in range(1, args.steps + 1):
        outputs = model(train_x)
        loss = loss_for(outputs, train_y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if step == 1 or step % 55 == 0:
            tool_acc = (outputs["tool"].argmax(dim=-1) == train_y["tool"]).float().mean().item()
            print(f"step {step:04d} loss {loss.item():.4f} train_tool_acc {tool_acc:.3f}")

    final = evaluate(model, TEST, device)
    summary = {
        "demo": "tool_call_sft",
        "data": "synthetic local-agent commands mapped to JSON tool calls",
        "device": str(device),
        "steps": args.steps,
        "initial_eval": initial,
        "final_eval": final,
        "tool_accuracy_delta": final["tool_accuracy"] - initial["tool_accuracy"],
        "exact_call_accuracy_delta": final["exact_call_accuracy"] - initial["exact_call_accuracy"],
        "note": "The model selects the schema and argument class; deterministic rendering keeps JSON valid.",
    }
    out = ensure_dir(args.out)
    torch.save({"model": model.state_dict(), "tools": TOOLS, "methods": METHODS, "splits": SPLITS, "formats": FORMATS, "paths": PATHS}, out / "checkpoint.pt")
    save_json(out / "summary.json", summary)
    print(summary)


if __name__ == "__main__":
    main()
