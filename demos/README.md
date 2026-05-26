# Laptop Training Demos

Laptop-scale runs for an Apple Silicon MacBook with 32 GB memory. Each run has a
train/eval split, measurable before/after results, a checkpoint, and a
`summary.json` file.

Run all quick checks:

```bash
python demos/run_all.py --quick
```

Run the fuller laptop demos:

```bash
python demos/run_all.py
```

Use a specific device when needed:

```bash
python demos/run_all.py --device cpu
python demos/run_all.py --device mps
```

Verified local run:

- Date: 2026-05-26.
- Command: `python demos/run_all.py --device mps`.
- Result summary: `demos/verified-results.md`.
- Artifacts: `outputs/demos/*/summary.json` and `outputs/demos/*/checkpoint.pt`.

## 00 Next-Token LM

Command:

```bash
python demos/00_next_token_lm/train_eval.py --steps 320
```

What it measures:

- initial held-out next-token loss;
- final train loss;
- final held-out next-token loss;
- held-out bits per token;
- a generated sample.

Why it matters:

Next-token training is the base objective behind decoder-only language models. A
tiny course-themed corpus keeps the evaluation text separate and saves both a
checkpoint and a readable summary.

## 01 Tool Router

Command:

```bash
python demos/01_tool_router/train_eval.py --steps 260
```

What it measures:

- held-out routing accuracy before and after training;
- JSON-valid tool call rate;
- per-example predictions.

Why it matters:

Small local models are often useful when the output space is narrow. A local tool
router can turn natural-language project commands into structured actions without
calling an external model.

## 02 RAG Reranker

Command:

```bash
python demos/02_rag_reranker/train_eval.py --steps 320
```

What it measures:

- held-out MRR;
- held-out top-1 accuracy;
- ranked documents before and after training.

Why it matters:

A useful local model does not have to generate text. A reranker can improve local
search or RAG by scoring query-document pairs and leaving the final answer step
to another component.

## 03 RLVR Arithmetic

Command:

```bash
python demos/03_rlvr_arithmetic/train_eval.py --steps 360
```

What it measures:

- exact-match accuracy over all one-digit addition problems before and after
  training;
- sample prompts, predicted answers, and verifier rewards.

Why it matters:

Verifiable rewards are appropriate when correctness can be checked by a program.
Training uses rewards computed by a deterministic verifier, not a stored
completion dataset. By default the verifier selects the best candidate in the
group for a stable laptop run; pass `--objective group-policy --sampled-group` to
inspect the noisier policy-gradient variant.

## Outputs

All demos write to:

```text
outputs/demos/<demo-name>/
  checkpoint.pt
  summary.json
```

Use `summary.json` as the first artifact to inspect in seminars. It records the
metric movement and enough examples to discuss whether training actually helped.
