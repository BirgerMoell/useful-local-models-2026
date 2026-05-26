# Model Menu And Compute Guidance

Re-verify model availability, licenses, and tooling shortly before the course
starts.

## Default Recommendation

For most generative projects, start with a small open model in the 0.5B-4B range
and train an adapter rather than a full model. The default named targets for
HT2026 should be Gemma 4 E2B/E4B and Qwen3.5 0.8B/2B/4B, with Qwen3-0.6B kept
as the fastest fallback.

Recommended default pattern:

```text
base model -> baseline prompting -> SFT with LoRA/QLoRA -> evaluation -> local export
```

Deviations from this pattern need a clear compute and evaluation reason.

## Candidate Model Families

### Gemma 4 Edge Models

Good for:

- local instruction tuning and adapter experiments;
- multimodal local tasks where images or audio are part of the research question;
- long-context experiments with a current open Google model;
- local deployment with Transformers, llama.cpp, MLX, Ollama, or related tools.

Known useful entry points:

- `google/gemma-4-E2B-it`
- `google/gemma-4-E4B-it`

Notes:

- Gemma 4 E2B and E4B are the named small-model targets for projects that need a
  modern Google model family.
- E2B is the standard starting point; E4B is stronger but needs more careful
  compute planning.
- Gemma access, license terms, gated downloads, and derivative release rules
  must be checked before public adapter release.

### Qwen3.5 Small Models

Good for:

- tiny-to-small local instruction tuning;
- multilingual and multimodal experiments;
- long-context and tool-call experiments;
- WebGPU, llama.cpp, Ollama, vLLM, SGLang, and Transformers deployment checks.

Known useful entry points:

- `Qwen/Qwen3.5-0.8B`
- `Qwen/Qwen3.5-2B`
- `Qwen/Qwen3.5-4B`

Notes:

- Qwen3.5-0.8B is the fastest named target for local experiments.
- Qwen3.5-2B is the likely default when quality matters but laptop feasibility
  still matters.
- Qwen3.5-4B is a strong upper-end course target; training requires a realistic
  GPU plan.
- Larger Qwen3.5 variants can be used for comparison or distillation, but not as
  the default training target.

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

- Qwen3-0.6B remains useful for fast experiments and laptop inference.
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

- Gemma 3 is a fallback when Gemma 4 access or tooling is inconvenient.
- Access may require accepting Google's terms.
- License and derivative-use restrictions must be checked carefully before a
  release is built around it.
- Prefer models with simpler open licenses for public adapter releases.

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

- LoRA on 0.5B-4B models;
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
| LoRA SFT | Default | Best balance of learning value and feasibility on Gemma 4/Qwen3.5-class models |
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
