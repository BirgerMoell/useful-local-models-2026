# Reading And Seminar Plan

Three reading seminars cover open training pipelines, fine-tuning, and advanced
local model methods. Each seminar can support 8-12 participants by assigning one
paper or section per person.

## Seminar 1: Open Training Pipelines And Artifacts

Theme:

How do we make model training auditable?

Core readings:

- Birger Moell. 2026. *The 2026 Fully Open LLM Training Guide*, sections 1-5,
  18-19.
  https://birgermoell.github.io/openeurollm-open-llm-guide/docs/fully-open-llm-guide-2026.pdf
- Mitchell et al. 2019. Model Cards for Model Reporting.
  https://arxiv.org/abs/1810.03993
- Hugging Face model card documentation.
  https://huggingface.co/docs/hub/model-cards
- Hugging Face dataset card documentation.
  https://huggingface.co/docs/datasets/v2.7.1/dataset_card

Optional readings:

- OLMo and Dolma papers/documentation.
- FineWeb/FineWeb-Edu documentation or paper.

Discussion questions:

- Which artifacts are necessary for scientific audit?
- What does "open" mean beyond downloadable weights?
- What data documentation is realistic in a student project?
- How should contamination be checked at course scale?

## Seminar 2: Fine-Tuning Small Local Models

Theme:

How can small models be adapted with limited compute?

Core readings:

- Hu et al. 2021. LoRA: Low-Rank Adaptation of Large Language Models.
  https://arxiv.org/abs/2106.09685
- Dettmers et al. 2023. QLoRA: Efficient Finetuning of Quantized LLMs.
  https://arxiv.org/abs/2305.14314
- Hugging Face PEFT documentation.
  https://huggingface.co/docs/transformers/peft
- Hugging Face TRL SFTTrainer documentation.
  https://huggingface.co/docs/trl/en/sft_trainer

Example local model documentation:

- nanochat.
  https://github.com/karpathy/nanochat
- Qwen3-0.6B.
  https://huggingface.co/Qwen/Qwen3-0.6B
- Qwen3-0.6B-GGUF local deployment.
  https://huggingface.co/Qwen/Qwen3-0.6B-GGUF

Discussion questions:

- What is actually trained in LoRA?
- When is SFT appropriate, and when is a classifier or reranker better?
- What should the baseline be?
- What are realistic compute constraints?

## Seminar 3: Advanced Techniques And Agent-Assisted Research

Theme:

When do context extension, DPO, GRPO/RLVR, and agent-assisted research make
sense?

Core readings:

- autoresearch.
  https://github.com/karpathy/autoresearch
- Rafailov et al. 2023. Direct Preference Optimization.
  https://arxiv.org/abs/2305.18290
- Shao et al. 2024. DeepSeekMath, for GRPO-style reasoning training.
  https://arxiv.org/abs/2402.03300
- DeepSeek-AI. 2025. DeepSeek-R1.
  https://arxiv.org/abs/2501.12948
- Peng et al. 2023. YaRN.
  https://arxiv.org/abs/2309.00071
- Ding et al. 2024. LongRoPE.
  https://arxiv.org/abs/2402.13753
- Yao et al. 2022. ReAct.
  https://arxiv.org/abs/2210.03629
- Schick et al. 2023. Toolformer.
  https://arxiv.org/abs/2302.04761

Discussion questions:

- What makes a reward verifiable?
- Why should GRPO/RLVR be restricted to tasks with objective rewards?
- How can a student evaluate actual long-context use rather than context length
  claims?
- What is the difference between tool-call formatting and true agent capability?
- What should an agent be allowed to edit, and what must the human review?
