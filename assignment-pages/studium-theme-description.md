# Studium Page: Theme Description

## Local Runnable Language Models

In this theme, we will study how to train small, useful, locally runnable language
models. The focus is not on using the largest available API model, but on the
research craft behind model development: data, adaptation, evaluation,
documentation, and release.

The guiding question is:

**Can we make small local models genuinely useful?**

Each project must include a real training or adaptation step. This may be LoRA or
QLoRA fine-tuning, full fine-tuning of a small model, continued pretraining,
instruction tuning, preference tuning, a trained classifier/reranker, or a small
experiment with verifiable rewards or tool use.

The final artifact should run locally without external API calls. It may be a
Transformers model, PEFT adapter, GGUF model for llama.cpp/Ollama, MLX model,
ONNX model, or another documented local format.

Possible project areas include Swedish and multilingual NLP, low-resource
adaptation, local RAG components, structured information extraction, small-model
instruction tuning, context extension, verifiable-reward training, and sandboxed
agentic tasks.

The key question for all projects is:

**Can a small local model be made genuinely useful for a specific language
technology task?**
