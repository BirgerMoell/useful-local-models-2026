# Local Deployment Guide

The final project artifact must run locally without external API calls.

## Acceptable Local Runtime Options

### Transformers + PEFT

Best for:

- adapters;
- research scripts;
- evaluation;
- students with Python/PyTorch familiarity.

Expected artifact:

- base model name and revision;
- PEFT adapter files;
- inference script;
- requirements file or environment notes.

### llama.cpp / GGUF

Best for:

- CPU or laptop inference;
- simple command-line demos;
- models that fit quantized.

Expected artifact:

- GGUF file or documented conversion path;
- quantization choice;
- llama-cli or llama-server command;
- sample prompt and output.

### Ollama

Best for:

- simple local demos;
- students who want an easy local serving interface.

Expected artifact:

- Modelfile or model reference;
- command to run;
- prompt template if needed.

### MLX

Best for:

- Apple Silicon machines.

Expected artifact:

- MLX-compatible model or conversion notes;
- command to run inference;
- memory estimate.

### ONNX / Small PyTorch / scikit-learn

Best for:

- classifiers;
- sequence taggers;
- rerankers;
- non-generative models.

Expected artifact:

- saved model;
- preprocessing pipeline;
- prediction script.

## Local Runnable Tiers

### Tier 1: Inspectable

The artifact can be loaded by the teacher or another student with documented
commands, but may require a GPU.

### Tier 2: Laptop Runnable

The artifact runs on a normal laptop CPU or Apple Silicon machine in quantized
form.

### Tier 3: Application Runnable

The artifact runs behind a local CLI, web UI, or OpenAI-compatible local server.

All projects must reach at least Tier 1. Strong projects reach Tier 2 or Tier 3.

## Reporting Local Performance

Students should report:

- runtime;
- model format;
- quantization;
- approximate disk size;
- memory used, if known;
- tokens per second or examples per second, if relevant;
- hardware used.

Example:

```text
Runtime: llama.cpp
Format: GGUF Q4_K_M
Model size: 1.2 GB
Hardware: MacBook Air M2, 16 GB RAM
Speed: 18 tokens/s, batch size 1
```

## Local Deployment Warnings

- Do not evaluate only the unquantized training checkpoint if the release model is
  quantized.
- Do not claim long-context support only because the config accepts longer input.
- Do not rely on a commercial API for final outputs.
- Do not publish private, copyrighted, or sensitive training data by accident.

