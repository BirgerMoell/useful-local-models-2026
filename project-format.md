# Project Format

## Basic Format

Projects are individual research projects with shared infrastructure.

Each student chooses a different task, language, dataset, or method, but every
project follows the same evidence format:

```text
research question
  -> data source registry
  -> baseline
  -> trained/adapted model
  -> evaluation
  -> local runnable artifact
  -> scientific report
```

The evidence chain is not a strict chronological order. A project may begin with
an evaluation task, a nanochat experiment, a local deployment target, or an
agent-assisted search loop. By the end, the evidence chain must be complete and
inspectable.

Teacher demos, example scripts, and project ideas are scaffolds. A student may
adapt them, but the submitted project still needs an independently formulated
research question and a student-owned angle.

## Required Project Shape

Every project must have:

1. A narrow use case where local execution matters.
2. A documented dataset or corpus.
3. A simple baseline.
4. A training or adaptation step that updates parameters.
5. A held-out evaluation.
6. A locally runnable final artifact.
7. A model card and dataset card.
8. A final paper.

## Shared Theme, Different Problems

Projects should not all train the same model on the same task. The shared method
is responsible training and evaluation of local models.

Good variation dimensions:

- language;
- domain;
- task;
- training method;
- evaluation design;
- deployment format;
- advanced technique.

## Standard Project

Recommended format for most projects:

```text
small open base model
  -> baseline prompting or classical baseline
  -> LoRA/QLoRA SFT or supervised model training
  -> held-out evaluation
  -> local inference script or adapter release
```

## Nanochat-Style Project

This format is useful when the student wants to understand the whole LLM stack at
small scale.

```text
nanochat or nanochat-inspired code
  -> small depth run
  -> one controlled change
  -> fixed-budget comparison
  -> eval/task report
```

The contribution can be an evaluation task, a data mixture change, a small SFT
ability, a local deployment recipe, or an analysis of a scaling/run result. The
student does not need to beat a leaderboard.

## Autoresearch-Style Project

This format is useful when the student wants to study agent-assisted research.

```text
agent program.md
  -> constrained write scope
  -> fixed-budget experiments
  -> experiment ledger
  -> human-reviewed conclusion
```

The scientific claim is not "the agent did research." The claim must be about
what changed, what metric moved, and whether the evidence supports keeping the
change.

Example:

```text
Qwen3-0.6B
  -> prompt baseline for Swedish form explanation
  -> LoRA SFT on curated examples
  -> evaluate factuality, readability, and format
  -> release PEFT adapter plus local run instructions
```

## Advanced Project

Advanced projects add one extra research component after the standard pipeline is
working.

Allowed advanced additions:

- continued pretraining;
- context extension;
- DPO or another preference method;
- GRPO/RLVR with verifiable rewards;
- sandboxed tool-use or agent training;
- quantization and deployment comparison;
- distillation into a smaller local model.

Advanced methods should answer a research question. They should not be included
only because they sound current.

## Group Infrastructure

The teacher can provide shared:

- model menu;
- starter repository;
- data/source registry template;
- evaluation checklist;
- local deployment guide;
- progress seminar structure.

Students still write individual proposals, train their own model or component,
and submit individual reports.

The supervisor may point students to datasets, shared tasks, papers, and broad
directions. The supervisor should not provide fully specified projects where the
research question, data choice, and method are already fixed.

## Recommended Limits

- Default model size: 0.5B-3B for causal LMs.
- Larger than 4B requires explicit approval.
- Advanced methods require a baseline and evaluation harness first.
- Final artifact must not depend on a commercial API.
- The project must be possible to explain in a 4-8 page paper.
