# Teacher Overview

## Theme

**Local Runnable Language Models: training small, useful, auditable NLP systems**

Students train or adapt open models for concrete NLP problems. The final result
must be a locally runnable artifact: an adapter, full fine-tune, classifier,
reranker, distilled model, GGUF export, or reproducible local inference script.

This theme is designed to fit the existing 5LN714 structure: literature seminars,
project proposal, progress seminars, first report, peer review, final workshop,
and final report.

## Official Course Anchor

The public Uppsala University course page lists 5LN714 as a 15-credit master's
level course. The current public syllabus and reading list are both marked as
valid from Spring 2026:

- Course page: <https://www.uu.se/en/study/course?query=5LN714>
- Syllabus: <https://www.uu.se/en/study/syllabus?query=52189>
- Reading list: <https://www.uu.se/en/study/reading-list?query=41226>

## Why This Theme

The current LLM landscape makes it easy for students to build impressive demos
with external APIs, but hard to learn the research craft behind models. This
theme shifts the center of gravity back to data, training, evaluation, and
release engineering.

The guiding question is:

**Can we make small local models genuinely useful?**

The 2026 update adds an explicit second question:

**How should students use AI agents as research collaborators while keeping the
work auditable?**

## Course-Level Learning Outcomes

By the end of the project, students should be able to:

- formulate a research question involving model training or adaptation;
- choose a feasible local model and justify its constraints;
- build a documented dataset or adaptation corpus;
- train a model or adapter using a reproducible recipe;
- compare against a meaningful baseline;
- evaluate with held-out data and appropriate metrics;
- document limitations, ethical risks, licenses, and compute cost;
- package the model so another person can run it locally.

## Scope Constraint

The course should not ask students to train a foundation model from scratch.
Instead, students should work with one of these feasible scopes:

- fine-tune a small causal LM with LoRA/QLoRA;
- train a small encoder model, classifier, reranker, or embedding model;
- continue-pretrain a small model on a limited corpus, then evaluate downstream;
- instruction-tune a small model for a focused task;
- apply DPO or another preference method after SFT;
- run a small GRPO/RLVR experiment with verifiable rewards;
- train a tool-use or agentic behavior on sandboxed tasks;
- compare quantized local deployment variants.
- run a nanochat-style fixed-budget experiment;
- use an autoresearch-style agent loop with a constrained write scope.

## Recommended Model Scale

Default:

- 0.5B-3B parameter causal LMs for instruction tuning and local inference.
- Smaller encoder models for classification, NER, retrieval, and reranking.

Upper bound:

- 4B parameters without special approval.
- Larger models only if the student has a strong reason and a feasible compute
  plan.

The final local artifact should ideally run on:

- a modern laptop CPU in quantized form;
- Apple Silicon with MLX or llama.cpp;
- a consumer GPU with 8-16 GB VRAM;
- UPPMAX for training, but not as the only way to inspect the final model.

## Required Project Artifact Set

Every student must submit or link:

1. Data source registry.
2. Train/dev/test split description.
3. Training configuration.
4. Baseline result.
5. Trained artifact.
6. Evaluation script or notebook.
7. Raw or summarized evaluation outputs.
8. Local run instructions.
9. Model card.
10. Dataset card or data statement.
11. Compute and energy estimate.
12. Ethical considerations.

## Suggested Instructor Policy

Students may use AI tools for coding assistance unless the course policy says
otherwise, but they must not submit AI-written prose as their own analysis. They
must document any AI assistance that materially affected code, data generation,
annotation, or analysis.

Peer-review papers should not be uploaded to external AI services unless
explicitly permitted by the course.

## Advanced Method Policy

Advanced techniques are encouraged only when the base training pipeline is stable.

Recommended evidence gates:

1. Baseline.
2. Data preparation and evaluation harness.
3. SFT or supervised training.
4. Local deployment.
5. Optional advanced method.

These gates do not have to be completed in this order. Students can begin with a
local deployment target, an evaluation task, or an agent experiment, but advanced
claims are not accepted without the relevant baseline and evaluation evidence.
