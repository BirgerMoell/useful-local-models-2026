# LM Course Code

Small utilities for the Local Runnable Language Models project theme.

The package is deliberately modest: project folders, experiment logs, and
artifact manifest validation without a required training framework.

## Commands

From this directory:

```bash
python -m lmcourse.cli init-project my-project --track sft
python -m lmcourse.cli validate-manifest my-project/artifact_manifest.yaml
python -m lmcourse.cli log-run my-project --metric val_bpb --value 0.782 --decision keep --note "baseline run"
python -m lmcourse.cli summarize-ledger my-project/logs/experiments.jsonl
```

## Intended Use

Works alongside:

- nanochat;
- autoresearch;
- Hugging Face Transformers/PEFT;
- custom PyTorch scripts;
- local deployment tools such as llama.cpp, Ollama, MLX, or ONNX.

## Design

- No heavy dependencies.
- Plain files over hidden state.
- Agent prompts are versioned in `agents/program.md`.
- Experiment logs are JSONL.
- Artifact manifests are YAML-like enough to inspect by eye.
