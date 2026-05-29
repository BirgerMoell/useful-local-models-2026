# Reading And Seminar Plan

The supervisor instructions for 2026 ask each theme to prepare three literature
seminars with three assigned articles per seminar. Students read all articles
for the seminar. Each student presents and leads discussion of one article during
the literature block, with a short presentation of at most 5 minutes.

If the group has fewer than nine students, the supervisor should cover the
remaining paper slots. Save around 15 minutes for project ideas in seminars 1
and 2, and use the extra time in seminar 3 for more concrete project scoping.

## Seminar 1: Open Training Pipelines And Artifacts

Theme:

How do we make model training auditable?

Assigned papers:

- Groeneveld et al. 2024. *OLMo: Accelerating the Science of Language Models*. https://arxiv.org/abs/2402.00838
- Soldaini et al. 2024. *Dolma: An Open Corpus of Three Trillion Tokens for Language Model Pretraining Research*. https://arxiv.org/abs/2402.00159
- Mitchell et al. 2019. *Model Cards for Model Reporting*. https://arxiv.org/abs/1810.03993

Discussion questions:

- Which artifacts are necessary for scientific audit?
- What does "open" mean beyond downloadable weights?
- What data documentation is realistic in a student project?
- How should contamination be checked at course scale?

## Seminar 2: Fine-Tuning Small Local Models

Theme:

How can small models be adapted with limited compute?

Assigned papers:

- Hu et al. 2021. *LoRA: Low-Rank Adaptation of Large Language Models*. https://arxiv.org/abs/2106.09685
- Dettmers et al. 2023. *QLoRA: Efficient Finetuning of Quantized LLMs*. https://arxiv.org/abs/2305.14314
- Ouyang et al. 2022. *Training Language Models to Follow Instructions with Human Feedback*. https://arxiv.org/abs/2203.02155

Discussion questions:

- What is actually trained in LoRA or QLoRA?
- When is SFT appropriate, and when is a classifier or reranker better?
- What should the baseline be?
- What are realistic compute constraints for student projects?

## Seminar 3: Advanced Techniques And Agent-Assisted Research

Theme:

When do context extension, DPO, GRPO/RLVR, and agent-assisted research make
sense?

Assigned papers:

- Rafailov et al. 2023. *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*. https://arxiv.org/abs/2305.18290
- Shao et al. 2024. *DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models*. https://arxiv.org/abs/2402.03300
- Peng et al. 2023. *YaRN: Efficient Context Window Extension of Large Language Models*. https://arxiv.org/abs/2309.00071

Discussion questions:

- What makes a reward verifiable?
- Why should GRPO/RLVR be restricted to tasks with objective rewards?
- How can a student evaluate actual long-context use rather than context length
  claims?
- What should an agent be allowed to edit, and what must the human review?

## Additional References For Project Inspiration

Use these as optional reading and project-scoping references. The list is longer
than the assigned seminar packet so students can find papers close to their own
task, language, or method.

- Birger Moell. 2026. *The 2026 Fully Open LLM Training Guide*. https://birgermoell.github.io/openeurollm-open-llm-guide/docs/fully-open-llm-guide-2026.pdf
- Karpathy. *nanochat*. https://github.com/karpathy/nanochat
- Karpathy. *autoresearch*. https://github.com/karpathy/autoresearch
- Hugging Face PEFT documentation. https://huggingface.co/docs/peft
- Hugging Face TRL SFTTrainer documentation. https://huggingface.co/docs/trl/sft_trainer
- Hugging Face TRL DPOTrainer documentation. https://huggingface.co/docs/trl/dpo_trainer
- Hugging Face TRL GRPOTrainer documentation. https://huggingface.co/docs/trl/grpo_trainer
- Hugging Face model card documentation. https://huggingface.co/docs/hub/model-cards
- Hugging Face dataset card documentation. https://huggingface.co/docs/datasets/dataset_card
- Qwen model documentation and small local checkpoints. https://huggingface.co/Qwen
- Gemma model documentation and local checkpoints. https://ai.google.dev/gemma
- Chen et al. 2023. *Extending Context Window of Large Language Models via Positional Interpolation*. https://arxiv.org/abs/2306.15595
- Ding et al. 2024. *LongRoPE: Extending LLM Context Window Beyond 2 Million Tokens*. https://arxiv.org/abs/2402.13753
- Hsieh et al. 2024. *RULER: What's the Real Context Size of Your Long-Context Language Models?* https://arxiv.org/abs/2404.06654
- Schick et al. 2023. *Toolformer: Language Models Can Teach Themselves to Use Tools*. https://arxiv.org/abs/2302.04761
- Yao et al. 2022. *ReAct: Synergizing Reasoning and Acting in Language Models*.
  https://arxiv.org/abs/2210.03629
- Khattab and Zaharia. 2020. *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT*. https://arxiv.org/abs/2004.12832
- Nogueira et al. 2020. *Document Ranking with a Pretrained Sequence-to-Sequence Model*. https://arxiv.org/abs/2003.06713
- Reimers and Gurevych. 2019. *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. https://arxiv.org/abs/1908.10084
- Wang et al. 2022. *Self-Instruct: Aligning Language Models with Self-Generated Instructions*. https://arxiv.org/abs/2212.10560
- Wei et al. 2021. *Finetuned Language Models Are Zero-Shot Learners*. https://arxiv.org/abs/2109.01652
- Bai et al. 2022. *Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback*. https://arxiv.org/abs/2204.05862
- Ziegler et al. 2019. *Fine-Tuning Language Models from Human Preferences*. https://arxiv.org/abs/1909.08593
- Cobbe et al. 2021. *Training Verifiers to Solve Math Word Problems*. https://arxiv.org/abs/2110.14168
- Wang et al. 2024. *Agentless: Demystifying LLM-based Software Engineering Agents*. https://arxiv.org/abs/2407.01489
