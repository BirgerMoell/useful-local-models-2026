# Student Project Brief

## Theme

**Local Runnable Language Models**

Build a small but serious language technology system by training or adapting a
model that can run locally. Your project may focus on different tasks,
languages, domains, or tooling. AI agents may help with coding and
experimentation. Every project follows the same research discipline: careful
data, explicit training, reproducible evaluation, and an artifact that another
person can run.

## Central Question

Can we make small local models genuinely useful?

Examples:

- Can a small Swedish model follow domain-specific instructions after instruction
  tuning?
- Does LoRA improve performance over prompting for a low-resource task?
- Can a local reranker improve search results without external APIs?
- Can a small model learn tool-call formatting reliably?
- Does context extension improve long-document QA, or only nominal context length?
- Can verifiable rewards improve reasoning on a narrow class of tasks?
- Can an agent-assisted experiment loop improve a model under a fixed budget?

## What Counts As Training

At least one part of your project must update model parameters. This may be:

- LoRA or QLoRA adapter training;
- full fine-tuning of a small model;
- continued pretraining on a domain corpus;
- supervised instruction tuning;
- DPO or another preference-tuning method;
- GRPO/RLVR with verifiable rewards;
- classifier, reranker, embedding, or sequence-labeling model training.

Prompt engineering alone is not enough.

## Suggested Small Models

Good default targets for generative projects:

- Gemma 4 E2B or E4B;
- Qwen3.5-0.8B, Qwen3.5-2B, or Qwen3.5-4B;
- Qwen3-0.6B for the fastest smoke tests and smallest hardware budgets.

The exact checkpoint must be justified by task, language coverage, license,
hardware, and local deployment format.

## Local Runnable Requirement

Your final system must run without calling a commercial API. Acceptable local
formats include:

- Hugging Face Transformers model or adapter;
- PEFT adapter plus base model;
- GGUF export for llama.cpp or Ollama;
- MLX model for Apple Silicon;
- ONNX or other local inference format;
- small scikit-learn or PyTorch model for non-generative tasks.

If the training itself requires UPPMAX, that is fine. The final artifact should
still be inspectable and runnable locally, or you must clearly justify why not.

## AI Agents

You may use AI agents for coding, debugging, experiment planning, and code
review. Agent use must be documented. If an agent materially changes code, data,
evaluation, or analysis, include the agent instructions and the experiment log in
your artifact package.

The final paper must be written in your own words.

## Minimum Deliverables

Your final project must include:

- a research question;
- related work;
- dataset description and source registry;
- baseline system;
- trained model or adapter;
- evaluation on held-out data;
- error analysis;
- significance testing where applicable;
- local run instructions;
- model card and dataset card;
- ethical considerations;
- final paper in the course format.

## Strong Projects

A strong project is not necessarily the one with the largest model. A strong
project has:

- a clear research question;
- a well-motivated task;
- documented data;
- a fair baseline;
- training decisions that are justified;
- evaluation that can reveal failures;
- honest discussion of limitations;
- a final artifact that actually runs.
