# Teacher Overview

## Theme

**Local Runnable Language Models: training small, useful, auditable NLP systems**

Students train or adapt open models for concrete NLP problems. The final result
must be a locally runnable artifact: an adapter, full fine-tune, classifier,
reranker, distilled model, GGUF export, or reproducible local inference script.

The project structure fits the existing 5LN714 rhythm: literature seminars,
project proposal, progress seminars, first report, peer review, final workshop,
and final report.

The HT2026 planning documents name Ellinor Lindqvist as course-responsible
teacher, Sara Stymne as examiner, and Birger Moell, Fredrik Wahlberg, Ellinor
Lindqvist, and Murathan Kurfali as teaching staff. The announced course period is
2026-08-31 to 2027-01-17.

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

**How can AI agents support research collaboration while keeping the work
auditable?**

## Course-Level Learning Outcomes

By the end of the project, each participant can:

- formulate a research question involving model training or adaptation;
- choose a feasible local model and justify its constraints;
- build a documented dataset or adaptation corpus;
- train a model or adapter using a reproducible recipe;
- compare against a meaningful baseline;
- evaluate with held-out data and appropriate metrics;
- document limitations, ethical risks, licenses, and compute cost;
- package the model so another person can run it locally.

## Scope Constraint

Foundation-model training from scratch is out of scope. Feasible project scopes
include:

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

- 0.5B-4B parameter causal LMs for instruction tuning and local inference.
- Gemma 4 E2B/E4B and Qwen3.5 0.8B/2B/4B as named small-model targets.
- Qwen3-0.6B as the fastest fallback for smoke tests and constrained hardware.
- Smaller encoder models for classification, NER, retrieval, and reranking.

Upper bound:

- 4B dense/effective parameters without special approval.
- Larger models only if the student has a strong reason and a feasible compute
  plan.

The final local artifact should ideally run on:

- a modern laptop CPU in quantized form;
- Apple Silicon with MLX or llama.cpp;
- a consumer GPU with 8-16 GB VRAM;
- UPPMAX for training, but not as the only way to inspect the final model.

## Supervisor Format For 2026

The supervisor role is to lead students through a research cycle, not to assign
fully specified projects. Students should formulate their own research questions
inside the theme. It is useful to pitch directions, datasets, shared tasks, and
project types, but the final angle should be the student's own.

Before the course starts, prepare:

- a 10-minute theme introduction for the first lecture;
- 1-2 paragraphs for the Studium theme page;
- three literature seminars with three assigned papers each;
- around 20-25 additional references for project inspiration;
- broad project directions, not ready-made project specifications.

The 2026 planning notes remove lab sessions from the course. Progress seminars
are therefore the main supervision venue. Do not schedule regular compulsory
extra meetings outside the seminar hours; answer questions by email or brief
meetings when needed.

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

AI tools may be used for coding assistance unless the course policy says
otherwise, but AI-written prose cannot stand in for the student's own analysis.
Any AI assistance that materially affects code, data generation, annotation, or
analysis must be documented.

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

These gates do not have to be completed in this order. A project can begin with a
local deployment target, an evaluation task, or an agent experiment, but advanced
claims are not accepted without the relevant baseline and evaluation evidence.
