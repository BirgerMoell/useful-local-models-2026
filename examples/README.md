# Tiny Training Examples

This directory is the code spine for the main question:

**Can we make small local models genuinely useful?**

Each directory contains a readable Python implementation of one modern
training idea with a tiny local model. The code uses synthetic data and a
character-level transformer so they can be inspected, modified, and run without
external APIs.

The code favors visibility over performance: the training loop should be easy to
read, change, and test.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install torch
```

Optional:

```bash
pip install matplotlib
```

## Examples

| Directory | Technique | What it shows |
|---|---|---|
| `01_pretraining` | next-token pretraining | base language-model training on tiny text |
| `02_instruction_tuning` | SFT | prompt/answer training for task behavior |
| `03_preference_dpo` | DPO | preference optimization after SFT-style behavior |
| `04_grpo_verifiable_rewards` | GRPO/RLVR | group-relative updates with exact-match rewards |
| `05_context_extension` | context extension | training short, adapting/evaluating longer context |
| `06_tool_use_sft` | tool-use SFT | structured tool-call output training |
| `07_reranker` | reranker training | local retrieval/reranking component |
| `08_local_inference` | local run path | loading a tiny checkpoint and generating locally |

## Quick Smoke Runs

From this folder:

```bash
python 01_pretraining/train.py --steps 80
python 02_instruction_tuning/train.py --steps 120
python 03_preference_dpo/train.py --steps 80
python 04_grpo_verifiable_rewards/train.py --steps 40
python 05_context_extension/train.py --steps 120
python 06_tool_use_sft/train.py --steps 120
python 07_reranker/train.py --steps 120
```

The scripts write small outputs under `outputs/`.

## How To Use These

Start by running one example unchanged, then change one thing:

- the data;
- the task;
- the model size;
- the context length;
- the reward function;
- the evaluation metric;
- the local runtime.

Each run should keep the same evidence discipline:

```text
use case -> baseline -> training -> held-out evaluation -> local artifact
```

## Relationship To Nanochat And Autoresearch

These runs are smaller than `nanochat` and easier to modify during a technical
seminar, progress session, or self-study run.
`nanochat` remains useful for inspecting a complete local LLM stack.
`autoresearch` remains useful for studying agent-assisted experimentation.

They give a common starting point before larger experiments branch out.
