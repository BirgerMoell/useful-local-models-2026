# Verified Laptop Results

Run date: 2026-05-27

Command:

```bash
python demos/run_all.py --device mps
```

Environment:

- Apple Silicon laptop target, 32 GB memory class.
- PyTorch 2.8.0.
- MPS available and used.
- Checkpoints and raw summaries written under `outputs/demos/`.

| Demo | Metric | Before | After | Change |
|---|---:|---:|---:|---:|
| Next-token LM | held-out loss | 117.240 | 3.303 | -113.937 |
| Next-token LM | held-out bits/token | 169.141 | 4.765 | -164.376 |
| Tool router | held-out accuracy | 0.20 | 1.00 | +0.80 |
| Tool router | JSON-valid tool calls | 1.00 | 1.00 | +0.00 |
| RAG reranker | MRR | 0.611 | 1.000 | +0.389 |
| RAG reranker | top-1 accuracy | 0.333 | 1.000 | +0.667 |
| RLVR arithmetic | exact accuracy | 0.10 | 1.00 | +0.90 |
| Course resource ranker | MRR | 0.250 | 1.000 | +0.750 |
| Course resource ranker | top-1 accuracy | 0.000 | 1.000 | +1.000 |
| Preference DPO | held-out preference accuracy | 0.250 | 1.000 | +0.750 |
| Tool-call SFT | held-out tool accuracy | 0.200 | 1.000 | +0.800 |
| Tool-call SFT | exact JSON-call accuracy | 0.200 | 1.000 | +0.800 |
| Context needle | exact accuracy | 0.0875 | 1.000 | +0.9125 |

Interpretation:

- The language-model run shows that the training loop lowers held-out
  next-token loss, but the generated sample is still low quality because the
  corpus and model are intentionally tiny.
- The tool router learns all held-out routing labels and keeps JSON validity at
  100%.
- The reranker moves every held-out query's relevant document to rank 1.
- The verifiable-reward arithmetic run moves from mostly wrong answers to exact
  answers on all one-digit addition pairs.
- The course resource ranker trains on the repo's Markdown course materials and
  learns to route held-out student questions to the right resource page.
- The DPO run changes held-out preference margins so chosen project-writing
  answers score above rejected overclaims.
- The tool-call SFT run learns the tool schema for local-agent commands and uses
  deterministic rendering to keep JSON valid.
- The context-needle run shows a tiny attention reader learning to select the
  right value from a longer key/value record.

The numbers are not intended as benchmark scores. They are smoke-test evidence
that the training code updates parameters, evaluates held-out behavior, and
writes inspectable artifacts on laptop hardware.
