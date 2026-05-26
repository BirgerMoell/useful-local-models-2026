# Project Tracks

Students may choose one primary track. Tracks can be combined, but only if the
basic supervised pipeline is working early.

## Track A: Local Instruction Tuning

**Difficulty:** standard

Train a small model to follow instructions in a specific task, language, or
domain.

Good for:

- Swedish administrative text;
- grammar feedback;
- OCR correction;
- information extraction;
- short summarization;
- domain-specific question answering;
- controlled style transfer.

Required method:

- baseline prompting or classical baseline;
- SFT with LoRA/QLoRA or full fine-tuning of a small model;
- local inference demo.

## Track B: Low-Resource or Multilingual Adaptation

**Difficulty:** standard to advanced

Adapt a multilingual model for a language or language pair with limited training
data.

Good for:

- NER;
- classification;
- parsing-related tasks;
- translation evaluation;
- cross-lingual transfer;
- language-specific instruction following.

Required method:

- report language coverage and tokenizer fertility where relevant;
- compare zero-shot/few-shot baseline to trained adaptation;
- evaluate by language, not only aggregate score.

## Track C: Retrieval, Reranking, and Local RAG Components

**Difficulty:** standard

Train a local component that improves retrieval or answer grounding.

Good for:

- reranking search results;
- training a domain embedding model;
- citation selection;
- hallucination detection;
- local document QA.

Required method:

- BM25 or embedding baseline;
- trained reranker/classifier/embedding model;
- evaluation with retrieval metrics and error analysis.

## Track D: Continued Pretraining or Mid-Training

**Difficulty:** advanced

Continue next-token training on a small domain corpus, then test whether it helps
downstream performance.

Good for:

- public-sector language;
- historical text;
- course-specific technical text;
- domain terminology;
- long-form document style.

Required method:

- domain corpus documentation;
- validation loss by domain;
- downstream evaluation before and after continued pretraining;
- check for regressions on a general task.

## Track E: Preference Tuning

**Difficulty:** advanced

After SFT, use preference pairs to train a model with DPO or a related method.

Good for:

- concise vs verbose answers;
- citation-grounded answers;
- safer completions;
- better structured outputs;
- style preference in Swedish or multilingual tasks.

Required method:

- SFT model or strong baseline;
- preference dataset with documented source;
- DPO or related preference method;
- evaluation that is not only a model-judge score.

## Track F: Verifiable Rewards and GRPO/RLVR

**Difficulty:** advanced, approval recommended

Train with rewards that can be automatically verified.

Good for:

- math with exact answers;
- code with unit tests;
- structured extraction with exact fields;
- database/query tasks;
- simple logic games;
- tool-use tasks with clear success/failure.

Required method:

- transparent reward function;
- sandboxed execution if code/tools are used;
- invalid-output and reward-hacking analysis;
- comparison against the SFT model.

## Track G: Context Extension and Long-Context Evaluation

**Difficulty:** advanced

Study whether a model can actually use longer context, not only accept a longer
token window.

Good for:

- long-document QA;
- multi-document synthesis;
- needle retrieval;
- lost-in-the-middle analysis;
- cross-lingual long context.

Required method:

- baseline at original context length;
- explicit context-extension or long-context adaptation method, if used;
- evaluation by context length and evidence position;
- short-context regression test.

## Track H: Agentic Local Models

**Difficulty:** advanced, approval recommended

Train or adapt a model for tool use in a sandboxed environment.

Good for:

- command selection;
- JSON tool-call formatting;
- simple coding repair;
- citation search;
- file transformation;
- spreadsheet/document microtasks.

Required method:

- tool schema;
- demonstration trajectories;
- sandbox or simulated tool environment;
- tool-call validity metric;
- task completion metric;
- permission/safety analysis.

