# Advanced Techniques Guide

Advanced methods are welcome, but they should be framed as research questions,
not decorations. Every advanced project still needs a baseline, supervised
training or adaptation, evaluation, and local deployment.

## Instruction Tuning

Instruction tuning is the default generative-model track.

Use when:

- the task can be expressed as input-output examples;
- the output format matters;
- prompting the base model is not reliable enough.

Minimum evidence:

- base model prompting baseline;
- SFT model result;
- held-out examples;
- error analysis.

## Continued Pretraining / Mid-Training

Use when:

- the goal is domain adaptation;
- the domain has terminology or style not well represented in the base model;
- downstream tasks may benefit from domain exposure.

Minimum evidence:

- validation loss before and after;
- downstream task before and after;
- at least one general regression check.

Avoid:

- training so long that the model overfits the corpus;
- claiming instruction-following improvement from next-token training alone.

## Context Extension

Use when:

- the task genuinely requires long input;
- evaluation can measure whether the model uses distant evidence.

Minimum evidence:

- baseline at original context length;
- evaluation by context length;
- evidence-position analysis;
- short-context regression check.

Course-scale options:

- long-context evaluation without training;
- light adaptation on long sequences;
- YaRN-style config experiment if supported by the model/tooling;
- retrieval-augmented alternative as a comparison.

Avoid:

- claiming success from config changes alone;
- using only one needle retrieval example;
- ignoring memory and KV-cache cost.

## Preference Tuning: DPO Or Similar

Use when:

- students have preference pairs;
- the desired behavior is comparative rather than exactly verifiable;
- SFT already works.

Minimum evidence:

- SFT baseline;
- preference dataset documentation;
- automatic and/or human evaluation;
- examples showing changed behavior.

Good preference dimensions:

- concise vs verbose;
- cites evidence vs unsupported answer;
- valid JSON vs malformed output;
- safe refusal vs unsafe compliance;
- domain-appropriate style.

Avoid:

- using noisy preference data without inspection;
- evaluating only with a model judge;
- treating DPO as a fix for missing task data.

## Verifiable Rewards: GRPO/RLVR

Use when:

- the reward can be checked automatically;
- the task has clear success/failure;
- the student can sandbox execution.

Good reward tasks:

- code problems with unit tests;
- math with exact answers;
- structured extraction with gold fields;
- SQL/query tasks with expected result;
- finite-state tool tasks;
- small logic games.

Minimum evidence:

- reward function code or pseudocode;
- reward distribution before training;
- comparison against SFT;
- invalid output rate;
- reward hacking analysis;
- pass@k where relevant.

Avoid:

- free-form LLM-as-judge rewards as the only signal;
- unsandboxed code execution;
- high-stakes domains;
- unclear reward functions.

## Agentic Tasks

Use when:

- the model must choose actions, call tools, or recover from tool errors;
- success can be checked in a sandbox.

Course-scale agent tasks:

- generate valid tool-call JSON;
- choose the correct tool from a small set;
- repair a small failing program with tests;
- answer with citations from a local document set;
- transform files using a simulated API;
- follow permission rules in a toy environment.

Minimum evidence:

- tool schema;
- trajectory format;
- tool-call validity;
- task completion;
- error recovery examples;
- safety and permission analysis.

Avoid:

- live destructive tools;
- browser or shell agents without sandboxing;
- relying on chat helpfulness as evidence of agent ability.

