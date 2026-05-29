# Milestones And Schedule

This schedule is aligned with the HT2026 planning proposal. The announced course
period is 2026-08-31 to 2027-01-17. Exact hand-in deadlines should still be
confirmed by the course coordinator before publication in Studium.

The 2026 planning notes remove lab sessions from the course. The theme should
therefore treat progress seminars as the main supervision setting.

## Schedule Anchors

| Date | Week | Slot | Planned Activity |
|---|---:|---|---|
| 2026-09-01 | 36 | Tue 10-12 | First lecture, roll-call registration, theme introductions |
| 2026-09-03 | 36 | Thu 13-15 | Full-class lecture |
| 2026-09-08 | 37 | Tue 8-10 | Full-class lecture / debate session |
| 2026-09-09 | 37 | Wed 10-12 | Literature seminar 1 |
| 2026-09-16 | 38 | Wed 9-12 | Philosophy/science theory examination slot, large room |
| 2026-09-22 | 39 | Tue 10-12 | Literature seminar 2 |
| 2026-09-28 | 40 | Mon 13-15 | Full-class lecture |
| 2026-09-29 | 40 | Tue 9-12 | Literature seminar 3 and extended project discussion |
| 2026-10-06 | 41 | Tue 10-12 | Full-class lecture |
| 2026-10-13 | 42 | Tue 9-12 | Proposal presentations |
| 2026-10-22 | 43 | Thu 10-12 | Full-class lecture |
| 2026-10-27 | 44 | Tue 10-12 | Progress seminar: data, baseline, first run |
| 2026-11-09 | 46 | Mon 10-12 | Full-class lecture |
| 2026-11-11 | 46 | Wed 10-12 | Progress seminar: training and early results |
| 2026-11-17 | 47 | Tue 10-12 | Full-class lecture |
| 2026-11-25 | 48 | Wed 10-12 | Progress seminar: ethics and release |
| 2026-12-07 | 50 | Mon 10-12 | Progress seminar: final analysis before paper submission |
| 2027-01-14 | 02 | Thu 9-16 | Final workshop with NLP, rooms 7-0042 and 7-0043 |

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

The teacher examples are starting points. Students should use them to understand
the shape of a feasible project, then formulate their own research question.

## Literature Seminar 1: Open Training Pipelines

Suggested date: 2026-09-09.

Focus:

- what a fully open training pipeline contains;
- data source registry;
- contamination control;
- model and dataset cards;
- local runnable release artifacts.

Student preparation:

- read all three assigned papers;
- prepare to discuss the artifacts each paper makes reproducible;
- identify one project idea or dataset direction the paper suggests.

## Literature Seminar 2: Fine-Tuning and Local Adaptation

Suggested date: 2026-09-22.

Focus:

- SFT;
- LoRA/QLoRA;
- small-model constraints;
- tokenizer/language issues;
- evaluation of adapted models.

Student preparation:

- explain what is updated during training;
- identify likely failure modes for small local models;
- bring one possible project direction.

## Literature Seminar 3: Advanced Local Model Techniques

Suggested date: 2026-09-29. Save extended time for project discussion.

Focus:

- DPO and preference tuning;
- context extension;
- GRPO/RLVR and verifiable rewards;
- tool use and agent tasks;
- safety and local deployment.

Student preparation:

- propose one advanced method and explain what evidence would show it worked;
- identify a simpler fallback project if the advanced method becomes infeasible.

## Proposal Deadline

The written proposal deadline should be set before 2026-10-13 so supervisors can
read proposals before the presentation seminar.

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

- Is the question formulated by the student?
- Is there a feasible baseline?
- Is at least one model parameter updated?
- Is the final artifact runnable locally?
- Is the data legally and ethically plausible?
- Is the advanced method optional or well justified?

## Proposal Presentation

Suggested date: 2026-10-13.

Students present:

- problem and why local model matters;
- data and model choice;
- training plan;
- evaluation;
- expected artifact.

Recommended timing:

- around 8 minutes presentation;
- short discussion and feasibility feedback.

For campus seminars, collect slides before the session when possible so students
can present from the teacher computer.

## Progress Seminar 1: Data And Baseline

Suggested date: 2026-10-27.

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

Suggested date: 2026-11-11.

Expected status:

- first supervised training run completed or actively running;
- training config documented;
- early evaluation result.

Students bring:

- training loss or metric plot;
- baseline vs trained-model comparison;
- known failure examples.

## Progress Seminar 3: Ethics And Release

Suggested date: 2026-11-25.

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

Suggested date: 2026-12-07.

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

Suggested date: 2027-01-14.

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
