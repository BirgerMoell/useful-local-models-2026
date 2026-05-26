# Modern Tooling Map

The theme should expose the current tooling ecosystem without making any single
tool mandatory. The guiding question stays:

**Can we make small local models genuinely useful?**

## Training And Adaptation

Use when the project needs to update parameters.

- Hugging Face Transformers: model loading, training, inference.
- PEFT: LoRA and adapter-based fine-tuning.
- TRL: SFT, DPO, and reinforcement-learning-oriented post-training.
- PyTorch: custom models, classifiers, rerankers, and research code.
- nanochat: readable full-stack system for tokenization, pretraining, SFT,
  eval, inference, RL, and chat.

## Local Runtime

Use when the final artifact needs to run without an external API.

- Transformers + PEFT adapter loading.
- llama.cpp and GGUF for CPU/laptop inference.
- Ollama for simple local serving.
- MLX for Apple Silicon.
- ONNX or plain PyTorch for classifiers and small task models.

## Evaluation

Use when a usefulness claim needs evidence.

- Task-specific held-out test sets.
- Hugging Face Evaluate for standard metrics.
- lm-evaluation-harness for language-model evals when appropriate.
- Custom JSONL evaluators for structured output, extraction, retrieval, or tool
  calls.
- Verifiers and unit tests for RLVR/GRPO-style projects.

## Agent-Assisted Research

Use when AI assistance can improve experimentation without hiding provenance.

- Codex, Claude Code, or similar coding agents for implementation and review.
- autoresearch for constrained agent experiment loops.
- `program.md` or equivalent files as versioned agent instructions.
- Experiment ledgers to record hypotheses, commands, metrics, and decisions.

## Data And Documentation

Use when the result needs auditable artifacts.

- Source registry CSV.
- Dataset cards.
- Model cards.
- Artifact manifests.
- Training configs and experiment logs.
- Local run instructions.

## Course Rule Of Thumb

The best tool is the one that makes the claim more testable. A tool that
produces impressive output but weakens provenance, evaluation, or local
runnability is the wrong tool for the project.
