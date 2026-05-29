# Teacher Start Checklist

Use this before the first project meeting.

## Before Course Start

- Verify the HT2026 course schedule against the proposed anchors: 2026-09-01 first lecture, 2026-10-13 proposal presentations, and 2027-01-14 final workshop.
- Verify UPPMAX project IDs and GPU access instructions.
- Decide whether students may publish adapters publicly or only submit them privately.
- Decide whether students may use AI coding assistants and how they should disclose that use.
- Decide whether all projects must reach laptop-runnable status or whether GPU-runnable local artifacts are acceptable.
- Verify current model licenses for the recommended model menu.
- Prepare the required 10-minute first-lecture theme pitch.
- Prepare the 3 x 3 literature seminar reading list plus 20-25 additional references.
- Prepare the Studium theme text, proposal text, progress-seminar text, and final report text.
- Prepare a small example repository or demo if desired, and make clear that it is a scaffold rather than a fixed student project.

## During Topic Selection

Collect from each student:

- preferred task/domain/language;
- hardware access;
- coding comfort;
- interest in advanced methods;
- whether they need a safer standard track;
- data access constraints.

## Approval Rules

Approve a project only if:

- there is a clear research question;
- the student has formulated the project angle themselves;
- the data source is plausible;
- the baseline is realistic;
- the training method is feasible;
- the evaluation can answer the research question;
- the final artifact can be run or inspected locally.

Require revision if:

- the project depends on a commercial API;
- the project is merely one of the teacher demos repeated without a new research question;
- the student wants to start with GRPO/agents before SFT or a baseline;
- there is no held-out evaluation;
- the data license is unclear;
- the model is too large for available compute.

## Supervision Boundaries

Progress seminars are the main supervision format. Each student should present
progress and a short plan for the next stage. Slides are optional unless they
need to show figures, results, or examples.

Do not require regular extra supervision meetings outside scheduled seminars.
Short email help or a brief meeting is fine when a student is blocked.

## Suggested Grouping

Projects can target different problems while sharing seminar infrastructure.
Group projects by method during progress seminars:

- SFT/local adaptation;
- retrieval/reranking/classification;
- multilingual/low-resource;
- context/pretraining;
- DPO/GRPO/agents.

## Teacher Feedback Phrases

Useful recurring prompts:

- What is the smallest model that can answer your research question?
- What would convince you that training helped?
- What is the baseline that would embarrass your model if it loses?
- What exactly can another student run locally?
- Which claim in your paper is least supported by evidence?
