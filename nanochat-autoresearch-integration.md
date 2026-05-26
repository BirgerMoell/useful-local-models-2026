# Worked Systems: Nanochat And Autoresearch

The guiding question is:

**Can we make small local models genuinely useful?**

`nanochat` and `autoresearch` give students two concrete systems to inspect: a
readable end-to-end local LLM stack and an agent-assisted experiment loop.

## What Nanochat Contributes

`karpathy/nanochat` is useful because it shows an entire LLM lifecycle in one
hackable codebase:

- tokenizer training;
- pretraining;
- supervised fine-tuning;
- evaluation;
- inference;
- reinforcement learning;
- chat CLI;
- web UI.

It is not the only code students should use, but it is the cleanest reference
example for the course philosophy: small enough to inspect, complete enough to
teach the real pipeline.

Use it as:

- show it in the first project meeting as the canonical "full stack" example;
- assign file-structure reading before the first technical lab;
- use `runs/runcpu.sh` or a small depth run as the accessible demo path;
- use `runs/speedrun.sh` as the ambitious full-stack reference, not as a
  requirement;
- use the `tasks/` structure as inspiration for student eval tasks;
- use `scripts/chat_sft.py`, `scripts/chat_eval.py`, and `scripts/chat_rl.py` as
  examples of staged post-training.

## What Autoresearch Contributes

`karpathy/autoresearch` is useful because it makes AI agents part of the research
workflow instead of a hidden shortcut.

Its core pattern is course-friendly:

```text
fixed training setup
  -> agent edits one constrained file
  -> fixed time-budget run
  -> metric decides whether the change helped
  -> experiment is logged
  -> human reviews the diff and the evidence
```

Use it as:

- teach `program.md` as an explicit agent instruction artifact;
- require students to disclose agent-generated code and analysis;
- require experiment logs rather than accepting "the agent improved it";
- keep agent write scopes small;
- compare agent suggestions against baselines and ablations;
- encourage students to ask agents for hypotheses, tests, and code review, not
  only implementation.

## The Course Adaptation

Students do not have to complete the whole LLM pipeline in order. Instead, each
project chooses a **research slice** and makes it auditable.

Possible slices:

- train a toy model from scratch using a nanochat-style setup;
- adapt a pretrained model with LoRA/QLoRA;
- add a new eval task inspired by nanochat `tasks/`;
- build an agent loop inspired by autoresearch;
- use agents to propose hyperparameter or architecture experiments;
- build a verifiable reward task;
- package the final model for local use.

## Required Agent-Use Discipline

If students use AI agents, they must submit:

- `agents/program.md` or equivalent agent instructions;
- `logs/experiments.jsonl`;
- a short disclosure of agent contribution;
- the human-reviewed final diff or artifact;
- a note on failed or rejected agent experiments.

## Example Course Agent Policy

Students may use AI agents for coding, debugging, experiment design, and
documentation scaffolding. They remain responsible for all submitted work. The
paper must be written in their own words. Any substantial agent contribution to
code, data generation, annotation, evaluation, or analysis must be disclosed in
the artifact manifest and final report.

Peer-review papers and confidential student work must not be uploaded to external
AI services.
