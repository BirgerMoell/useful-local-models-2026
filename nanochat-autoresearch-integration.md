# Worked Systems: Nanochat And Autoresearch

The guiding question is:

**Can we make small local models genuinely useful?**

`nanochat` and `autoresearch` give two concrete systems to inspect: a readable
end-to-end local LLM stack and an agent-assisted experiment loop.

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

It is not a required base, but it is a useful reference implementation: compact
enough to inspect, complete enough to show the real pipeline.

Useful roles:

- first-pass map of a full local training stack;
- file-structure reading before the first technical seminar or demo;
- use `runs/runcpu.sh` or a small depth run as the accessible demo path;
- use `runs/speedrun.sh` as the ambitious full-stack reference, not as a
  requirement;
- use the `tasks/` structure as inspiration for evaluation tasks;
- use `scripts/chat_sft.py`, `scripts/chat_eval.py`, and `scripts/chat_rl.py` as
  examples of staged post-training.

## What Autoresearch Contributes

`karpathy/autoresearch` is useful because it makes AI agents part of the research
workflow instead of a hidden shortcut.

Its core pattern is auditable:

```text
fixed training setup
  -> agent edits one constrained file
  -> fixed time-budget run
  -> metric decides whether the change helped
  -> experiment is logged
  -> human reviews the diff and the evidence
```

Useful roles:

- treat `program.md` as an explicit agent instruction artifact;
- disclose agent-generated code and analysis;
- keep experiment logs rather than accepting "the agent improved it";
- keep agent write scopes small;
- compare agent suggestions against baselines and ablations;
- ask agents for hypotheses, tests, and code review, not only implementation.

## Project Adaptation

The whole LLM pipeline does not have to be completed in order. A good project
chooses a **research slice** and makes it auditable.

Possible slices:

- train a small model from scratch using a nanochat-style setup;
- adapt a pretrained model with LoRA/QLoRA;
- add a new eval task inspired by nanochat `tasks/`;
- build an agent loop inspired by autoresearch;
- use agents to propose hyperparameter or architecture experiments;
- build a verifiable reward task;
- package the final model for local use.

## Required Agent-Use Discipline

When AI agents materially affect the work, the artifact set should include:

- `agents/program.md` or equivalent agent instructions;
- `logs/experiments.jsonl`;
- a short disclosure of agent contribution;
- the human-reviewed final diff or artifact;
- a note on failed or rejected agent experiments.

## Agent-Use Policy

AI agents may be used for coding, debugging, experiment design, and
documentation scaffolding. The submitted analysis remains the author's
responsibility. Any substantial agent contribution to code, data generation,
annotation, evaluation, or analysis should be disclosed in the artifact manifest
and final report.

Peer-review papers and confidential work must not be uploaded to external AI
services.
