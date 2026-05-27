# Laptop Training Demos

Laptop-scale runs for an Apple Silicon MacBook with 32 GB memory. Each run has a
train/eval split, measurable before/after results, a checkpoint, and a
`summary.json` file.

The suite mixes one real corpus with controlled synthetic tasks:

- Real corpus: course Markdown resources are used as a local document collection
  for a trained resource reranker.
- Synthetic task data: preference pairs, tool-call commands, arithmetic rewards,
  and long-record key/value facts are generated so the expected answer is known
  and the training signal is inspectable.

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

- Date: 2026-05-27.
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

## 04 Course Resource Ranker

Command:

```bash
python demos/04_course_resource_ranker/train_eval.py --steps 260
```

What it measures:

- held-out MRR and top-1 accuracy over course-resource search queries;
- ranked resource pages before and after training;
- whether the model can use the real Markdown corpus plus small query labels.

Why it matters:

This is the most course-like demo. The corpus is not invented text: it is the
repository's own project brief, rubric, model menu, deployment guide, Studium
assignment pages, and templates. Students can adapt the pattern to build a local
course assistant, documentation search layer, or project-resource navigator.

## 05 Preference DPO

Command:

```bash
python demos/05_preference_dpo/train_eval.py --steps 120
```

What it measures:

- held-out preference accuracy;
- chosen-vs-rejected log-probability margins before and after DPO;
- whether the policy assigns higher probability to safer, more specific project
  writing than to overclaimed alternatives.

Why it matters:

DPO gives students a minimal preference-tuning loop. The demo keeps the data
small enough to read by hand, while still saving a real checkpoint and showing
how relative quality can be trained without a separate reward model.

## 06 Tool-Call SFT

Command:

```bash
python demos/06_tool_call_sft/train_eval.py --steps 220
```

What it measures:

- held-out tool accuracy;
- exact JSON-call accuracy;
- JSON validity after deterministic rendering.

Why it matters:

Useful local models often sit inside a larger system. This demo trains a small
schema selector for local-agent commands, then renders valid JSON calls for
search, training, evaluation, export, and inspection. It is a practical starting
point for narrow agentic tasks.

## 07 Context Needle

Command:

```bash
python demos/07_context_needle/train_eval.py --steps 260
```

What it measures:

- exact answer accuracy on held-out long records;
- examples where the model must return the value attached to the queried slot;
- whether the trained attention reader learns which slot to select.

Why it matters:

Long-context claims need tasks where distant evidence matters. This demo parses a
long key/value record into slot features, then trains a small attention reader to
select the queried slot. It is intentionally tiny, but it shows the evaluation
shape students need before claiming context extension helped.

## Outputs

All demos write to:

```text
outputs/demos/<demo-name>/
  checkpoint.pt
  summary.json
```

Use `summary.json` as the first artifact to inspect in seminars. It records the
metric movement and enough examples to discuss whether training actually helped.
