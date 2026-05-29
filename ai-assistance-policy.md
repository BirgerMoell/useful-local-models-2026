# AI Assistance And Research Integrity

Students may use modern AI tools during the project, including coding agents,
local assistants, autocomplete, and model-based debugging tools. The point is to
learn how to use these tools as part of a research workflow, while keeping the
scientific claims accountable.

## Allowed Uses

AI tools may be used for:

- exploring implementation options;
- writing or revising code;
- debugging training and evaluation scripts;
- generating small synthetic examples for pilots;
- drafting experiment plans or checklists;
- checking whether documentation is understandable;
- summarizing public papers or public documentation for personal use.

Every submitted claim must still be supported by data, baselines, held-out
evaluation, logs, and human inspection. A tool suggestion is not evidence.

## Required Disclosure

In the proposal, first report, and final report, include a short AI assistance
statement if AI tools were used. State:

- which tools were used;
- what they helped with;
- which generated code, prompts, data, or text were kept;
- how the student checked correctness.

Example:

I used Codex to draft an evaluation script and to debug a tensor-shape error. I
reviewed and edited the code, ran the final experiments myself, and report only
results from the saved evaluation logs.

## Not Allowed

Do not use AI tools to:

- fabricate citations, experiments, results, or error analyses;
- submit text that the student has not checked and rewritten in their own words;
- upload confidential peer papers, unpublished student work, private datasets,
  access tokens, or personal data to external services;
- hide which parts of the project were assisted by tools;
- claim that a model is useful without comparing it to a baseline and testing it
  on held-out examples.

Peer review is a special case. Unless the course coordinator explicitly changes
the policy, peer papers should not be uploaded to external AI tools or reviewed
with AI assistance, because they are confidential student work.

## Good Practice

Keep useful traces when they help another person understand the project:

- important prompts;
- generated diffs that were accepted;
- failed experiment notes;
- final configs;
- environment details;
- saved metrics and representative outputs.

Do not include secrets, private data, or unnecessary chat transcripts in the
submitted artifact.

## What To Grade

Grade the scientific work, not the tool performance. Strong projects use AI
assistance to move faster while still showing independent judgment: clear
research questions, careful baselines, reproducible training, honest evaluation,
and thoughtful limitations.
