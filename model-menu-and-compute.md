# Model Menu And Compute Guidance

This menu should be verified shortly before the course starts. Model availability,
licenses, and tooling change quickly.

## Default Recommendation

For most generative projects, start with a small open model in the 0.5B-3B range
and train an adapter rather than a full model.

Recommended default pattern:

```text
base model -> baseline prompting -> SFT with LoRA/QLoRA -> evaluation -> local export
```

Students should justify deviations from this pattern.

## Candidate Model Families

### Qwen3 Small Models

Good for:

- instruction tuning;
- reasoning/no-reasoning comparisons;
- multilingual experiments;
- local GGUF/Ollama/llama.cpp deployment.

Known useful entry point:

- `Qwen/Qwen3-0.6B`
- `Qwen/Qwen3-0.6B-GGUF`
- `Qwen/Qwen3-4B`

Notes:

- Qwen3-0.6B is especially useful for fast experiments and laptop inference.
- Qwen3-4B is a stronger upper-end option but should be treated as advanced for
  training.
- Verify license and exact model variant before assigning.

### SmolLM3

Good for:

- small-model reasoning;
- local deployment;
- projects where Apache-2.0 licensing is important;
- comparing long-context claims against actual performance.

Known useful entry point:

- `HuggingFaceTB/SmolLM3-3B`
- GGUF variants are available through the Hugging Face ecosystem.

Notes:

- Strong candidate for course use because it is explicitly positioned as a small,
  open local model.
- Students should still test whether the language/task coverage fits their
  project.

### Gemma 3 Small Models

Good for:

- lightweight local inference;
- multilingual text generation;
- comparison experiments.

Known useful entry point:

- `google/gemma-3-1b-it`

Notes:

- Access may require accepting Google's terms.
- License and derivative-use restrictions must be checked carefully before a
  student builds a release around it.
- Prefer models with simpler open licenses if students will publish adapters.

### Encoder Models

Good for:

- classification;
- NER;
- reranking;
- embedding;
- retrieval;
- hallucination detection.

Students do not need a causal LM if an encoder model is a better research fit.
Small encoder projects are often stronger scientifically because evaluation is
cleaner.

## Training Budget Tiers

### Tier A: Laptop / CPU-Friendly

Suitable for:

- classical baselines;
- small classifiers;
- evaluation;
- GGUF inference;
- very small fine-tunes.

Expected final artifact:

- local script or quantized model.

### Tier B: Consumer GPU / Apple Silicon

Suitable for:

- LoRA on 0.5B-3B models;
- small encoder fine-tuning;
- reranker training;
- short SFT runs.

Expected final artifact:

- PEFT adapter, MLX model, or GGUF export.

### Tier C: UPPMAX GPU

Suitable for:

- longer SFT runs;
- QLoRA on larger models;
- continued pretraining;
- DPO;
- small GRPO/RLVR experiments.

Expected final artifact:

- still locally inspectable, even if training required cluster compute.

## Method Feasibility

| Method | Course Feasibility | Notes |
|---|---|---|
| Baseline prompting | Required for generative tasks | Cheap and necessary |
| LoRA SFT | Default | Best balance of learning value and feasibility |
| QLoRA SFT | Default for larger local models | Requires GPU/tooling care |
| Full fine-tuning | Only for very small models | Higher risk of compute and instability |
| Continued pretraining | Advanced | Needs careful evaluation to prove usefulness |
| DPO | Advanced | Needs preference pairs and SFT baseline |
| Context extension | Advanced | Must evaluate actual long-context behavior |
| GRPO/RLVR | Advanced | Only with verifiable rewards |
| Agent training | Advanced | Use sandboxed tasks only |

## Hard Constraints For Students

- No commercial API as the final model.
- No private tokens, secrets, or copyrighted data in repositories.
- No live destructive tools in agent projects.
- No advanced method without a baseline and evaluation harness.
- No unsupported claims such as "works in Swedish" without Swedish evaluation.

