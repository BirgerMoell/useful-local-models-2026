# Rubric

This rubric is intended for the project theme. It can be used inside the existing
course assessment structure without changing the course-level assignment weights.

## Proposal Rubric

| Criterion | Pass | Strong/Distinction-Level |
|---|---|---|
| Research question | Clear enough to guide a project | Precise, testable, and motivated by prior work |
| Feasibility | Model, data, and compute are plausible | Includes fallback plan and scoped advanced option |
| Data plan | Identifies sources and split strategy | Includes source registry, licensing, contamination risks |
| Training plan | Includes parameter update | Justifies model, method, hyperparameters, and constraints |
| Evaluation plan | Has baseline and held-out test | Metrics expose likely failure modes |
| Local deployment | States how model will run locally | Includes target hardware and export format |
| Ethics | Mentions relevant risks | Connects risks to concrete mitigations |

## Final Paper Rubric

| Criterion | Weight | Expectations |
|---|---:|---|
| Research framing | 15 | Clear question, motivation, and relation to prior work |
| Data and governance | 15 | Source registry, splits, licensing, quality, leakage checks |
| Training method | 20 | Reproducible config, justified model choice, clear training description |
| Evaluation | 20 | Baseline, held-out results, metrics, significance testing where applicable |
| Analysis | 15 | Error analysis, limitations, failed attempts, interpretation |
| Local artifact and documentation | 10 | Model card, dataset card, manifest, local run instructions |
| Writing and structure | 5 | Scientific clarity, citations, TACL-style organization |

## Artifact Rubric

| Criterion | Pass | Strong/Distinction-Level |
|---|---|---|
| Runs locally | Basic local run path documented | Another student can reproduce on stated hardware |
| Reproducibility | Configs and commands included | Versioned data recipe, seeds, logs, and eval outputs included |
| Model documentation | Model card present | Card separates verified claims from limitations and hypotheses |
| Dataset documentation | Dataset card or data statement present | Includes license, source, filtering, splits, and known bias |
| Evaluation package | Results reported | Scripts or notebooks allow rerunning evaluation |
| Safety | Basic risk note | Concrete safety, privacy, and misuse analysis |

## Presentation Rubric

| Criterion | Expectations |
|---|---|
| Research story | The audience understands the problem and why training was needed |
| Method | Model, data, and training are explained without unnecessary detail |
| Evidence | Main result is clear and tied to the research question |
| Local artifact | The local runnable nature of the model is demonstrated or documented |
| Reflection | Limitations and next steps are honest |

## Minimum Pass Conditions

A project should normally not pass if:

- no model parameters were trained or adapted;
- there is no meaningful baseline;
- evaluation is only anecdotal;
- the final artifact cannot be inspected or run in any documented way;
- data provenance is unclear;
- the report makes model capability claims unsupported by evaluation.

