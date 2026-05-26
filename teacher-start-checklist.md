# Teacher Start Checklist

Use this before the first project meeting.

## Before Course Start

- Verify the current course schedule and replace placeholder dates.
- Verify UPPMAX project IDs and GPU access instructions.
- Decide whether students may publish adapters publicly or only submit them
  privately.
- Decide whether students may use AI coding assistants and how they should
  disclose that use.
- Decide whether all projects must reach laptop-runnable status or whether
  GPU-runnable local artifacts are acceptable.
- Verify current model licenses for the recommended model menu.
- Prepare a small example repository or demo if desired.

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
- the data source is plausible;
- the baseline is realistic;
- the training method is feasible;
- the evaluation can answer the research question;
- the final artifact can be run or inspected locally.

Require revision if:

- the project depends on a commercial API;
- the student wants to start with GRPO/agents before SFT or a baseline;
- there is no held-out evaluation;
- the data license is unclear;
- the model is too large for available compute.

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
