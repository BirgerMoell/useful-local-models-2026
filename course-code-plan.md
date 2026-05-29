# Course Code Plan

The code around the project materials stays small and inspectable. The primary
asset is a set of readable training runs that are easy to execute, inspect, and
modify.

## Code Layers

### 1. Tiny Training Examples

Location:

```text
examples/
```

Purpose:

- show hello-world versions of modern training techniques;
- provide concrete Python files that can be modified;
- keep examples small enough for a seminar demo or self-study run;
- separate technique examples by folder.

Current examples:

- next-token pretraining;
- instruction tuning;
- DPO;
- GRPO/RLVR with verifiable rewards;
- context extension;
- tool-use SFT;
- reranker training;
- local inference.

### 2. Optional Course Project CLI

Location:

```text
course-code/
```

Purpose:

- initialize student project folders;
- copy templates;
- validate artifact manifests;
- append experiment logs;
- summarize experiment ledgers.

The optional utility code stays as a small Python package with no required
third-party dependencies.

### 3. Starter Project Structure

Every initialized project has:

```text
agents/
  program.md
cards/
  model_card.md
  dataset_card.md
configs/
  project.yaml
  train.yaml
  eval.yaml
data/
  source_registry.csv
logs/
  experiments.jsonl
outputs/
src/
  README.md
artifact_manifest.yaml
README.md
```

### 4. Agent Program Templates

Agent prompts are versioned research artifacts.

Templates include:

- standard supervised training assistant;
- nanochat-style experiment assistant;
- autoresearch-style constrained code editor;
- eval/task builder;
- code reviewer.

### 5. Experiment Ledger

Each run is logged as JSONL:

```json
{"run_id":"2026-09-21-001","hypothesis":"lower lr improves validation bpb","metric":"val_bpb","value":0.751,"decision":"keep"}
```

The ledger captures:

- hypothesis;
- code/config change;
- data version;
- runtime;
- metric;
- decision;
- agent involvement.

### 6. Nanochat Examples

Lightweight examples point to `nanochat` rather than vendoring it:

- a reading guide for the repo structure;
- a small `depth` run recipe;
- a CPU/MPS demonstration recipe;
- a task-writing exercise inspired by `tasks/customjson.py`;
- an eval interpretation worksheet.

### 7. Autoresearch Examples

The course should include:

- a `program.md` template;
- a constrained-write-scope policy;
- a fixed-budget experiment recipe;
- an agent disclosure template;
- a human review checklist.

### 8. Optional Future Additions

These can be built if the theme becomes a recurring course component:

- a tiny web dashboard for experiment ledgers;
- a local model demo app template;
- a Slurm script generator for UPPMAX;
- a Hugging Face model-card generator;
- a GGUF export helper;
- a lightweight eval harness for JSONL tasks.

## Current Implementation Status

The current pack includes:

- static course page in `site/`;
- tiny training examples in `examples/`;
- `lmcourse` CLI skeleton in `course-code/`;
- templates for project initialization;
- documentation for nanochat/autoresearch integration.
