# Milestones And Schedule

The schedule fits the normal 5LN714 rhythm. Replace dates with the final HT2026
course dates when they are known.

## Before Project Choice

Students receive:

- theme description;
- project tracks;
- feasible model list;
- compute expectations;
- examples of strong and weak project scopes.

Students submit:

- ranked project interests;
- hardware access note;
- preferred task/language/domain.

## Literature Seminar 1: Open Training Pipelines

Focus:

- what a fully open training pipeline contains;
- data source registry;
- contamination control;
- model and dataset cards;
- local runnable release artifacts.

Student preparation:

- read assigned paper/section;
- identify one artifact the paper makes reproducible and one artifact it does
  not expose clearly.

## Literature Seminar 2: Fine-Tuning and Local Adaptation

Focus:

- SFT;
- LoRA/QLoRA;
- small-model constraints;
- tokenizer/language issues;
- evaluation of adapted models.

Student preparation:

- explain what is updated during training;
- identify likely failure modes for small local models.

## Literature Seminar 3: Advanced Local Model Techniques

Focus:

- DPO and preference tuning;
- context extension;
- GRPO/RLVR and verifiable rewards;
- tool use and agent tasks;
- safety and local deployment.

Student preparation:

- propose one advanced method and explain what evidence would show it worked.

## Proposal Deadline

Proposal must include:

- research question;
- local-use case;
- dataset plan;
- baseline;
- model and training plan;
- evaluation plan;
- local deployment plan;
- risk and fallback plan.

Instructor check:

- Is there a feasible baseline?
- Is at least one model parameter updated?
- Is the final artifact runnable locally?
- Is the data legally and ethically plausible?
- Is the advanced method optional or well justified?

## Proposal Presentation

Students present:

- problem and why local model matters;
- data and model choice;
- training plan;
- evaluation;
- expected artifact.

Recommended timing:

- 8 minutes presentation;
- 4 minutes discussion.

## Progress Seminar 1: Data And Baseline

Expected status:

- data source registry started;
- train/dev/test split planned or created;
- baseline running;
- evaluation script draft.

Students bring:

- one example input/output;
- first baseline number or clear blocker;
- one risk needing feedback.

## Progress Seminar 2: Training Run

Expected status:

- first supervised training run completed or actively running;
- training config documented;
- early evaluation result.

Students bring:

- training loss or metric plot;
- baseline vs trained-model comparison;
- known failure examples.

## Progress Seminar 3: Ethics And Release

Expected status:

- ethical considerations draft;
- model/dataset card draft;
- local deployment plan.

Discussion topics:

- data rights;
- PII and sensitive content;
- bias and language coverage;
- environmental cost;
- misuse and safety;
- whether the model card overclaims.

## Progress Seminar 4: Final Analysis

Expected status:

- final training complete;
- evaluation complete or nearly complete;
- local demo working;
- paper outline complete.

Students bring:

- main result table;
- error categories;
- final artifact manifest draft.

## First Report

The first report should be a complete scientific paper. It may still have rough
analysis, but no section should be missing.

Must include:

- research question;
- related work;
- data;
- model/training method;
- baseline;
- evaluation;
- results;
- error analysis;
- ethical considerations;
- artifact availability statement.

## Peer Review

Reviewers should evaluate both the scientific paper and the reproducibility of
the artifact claims.

Reviewers should not run unsafe code. They may inspect README files, configs,
cards, and reported outputs.

## Final Workshop

Presentation should include:

- motivation;
- method;
- one concrete local demo screenshot or transcript;
- main result;
- strongest limitation;
- what changed after peer review.

## Final Report

Final report must include:

- revised scientific paper;
- response to review comments;
- final model/dataset documentation;
- final artifact manifest;
- local run instructions.
