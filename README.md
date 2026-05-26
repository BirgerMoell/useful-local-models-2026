# Local Runnable Language Models: Course Project Pack

This folder contains a ready-to-adapt project theme for 5LN714 Language Technology:
Research and Development, intended for HT2026.

Site: https://birgermoell.github.io/useful-local-models-2026/

Official course anchors checked on 2026-05-26:

- Course page: https://www.uu.se/en/study/course?query=5LN714
- Syllabus valid from Spring 2026: https://www.uu.se/en/study/syllabus?query=52189
- Reading list valid from Spring 2026: https://www.uu.se/en/study/reading-list?query=41226

The theme is:

**Local Runnable Language Models: training small, useful, auditable NLP systems**

The core idea is model ownership rather than API-only experimentation: train or
adapt a model, evaluate it carefully, and release a small artifact that can run
locally without an external API.

The guiding question is:

**Can we make small local models genuinely useful?**

## Recommended Use

Use these files as a teacher-facing pack:

- `site/index.html`: polished landing page with all resources.
- `teacher-overview.md`: high-level course design and teacher guidance.
- `student-project-brief.md`: student-facing project description.
- `project-format.md`: the required shape of each student project.
- `modern-tooling-map.md`: broad 2026 tooling map for training, eval, agents, and local runtime.
- `model-menu-and-compute.md`: feasible model and compute guidance.
- `teacher-start-checklist.md`: setup and approval checklist.
- `project-tracks.md`: suggested project tracks and difficulty levels.
- `milestones-and-schedule.md`: how to fit the theme into the existing 5LN714 flow.
- `rubric.md`: assessment rubric for proposals, papers, presentations, and artifacts.
- `reading-and-seminar-plan.md`: literature seminar structure.
- `training-pipeline-spec.md`: required technical artifacts for every project.
- `local-deployment-guide.md`: local inference and quantization expectations.
- `advanced-techniques-guide.md`: context extension, DPO, GRPO/RLVR, and agents.
- `nanochat-autoresearch-integration.md`: worked systems from nanochat and autoresearch.
- `course-code-plan.md`: code infrastructure needed for the course.
- `project-ideas.md`: concrete project suggestions for topic selection.
- `examples/`: tiny PyTorch hello-world training examples for course techniques.
- `demos/`: laptop-runnable training demos with train/eval metrics.
- `slides/` and `site/slides/`: presentation plan and web slide decks.
- `assignment-pages/`: Studium-ready assignment text.
- `templates/`: proposal, model card, dataset card, manifest, experiment log.
- `starter-repo/`: a lightweight repository skeleton for project setup.
- `course-code/`: optional utility code for project scaffolds and experiment ledgers.

## Design Principles

1. Every claim maps to an artifact: data manifest, config, checkpoint, adapter,
   evaluation output, log, or model card.
2. Local runnable beats impressive but opaque. A useful 0.6B-4B model with honest
   evaluation is preferred over an API demo.
3. The pipeline does not have to be completed in order. Each research slice still
   needs a baseline, evidence, and a local artifact.
4. Evaluation matters as much as training. Each project compares against a
   baseline and analyzes errors.
5. The final artifact should be usable by another student on ordinary hardware,
   or the student must explain why a stronger machine is required.

## Main Sources

- Uppsala University 5LN714 course page:
  https://www.uu.se/en/study/course?query=5LN714
- Uppsala University 5LN714 syllabus, valid from Spring 2026:
  https://www.uu.se/en/study/syllabus?query=52189
- Uppsala University 5LN714 reading list, valid from Spring 2026:
  https://www.uu.se/en/study/reading-list?query=41226
- Birger Moell, *The 2026 Fully Open LLM Training Guide*:
  https://birgermoell.github.io/openeurollm-open-llm-guide/docs/fully-open-llm-guide-2026.pdf
- Hugging Face PEFT:
  https://huggingface.co/docs/transformers/peft
- Hugging Face model cards:
  https://huggingface.co/docs/hub/model-cards
- Hugging Face dataset cards:
  https://huggingface.co/docs/datasets/v2.7.1/dataset_card
- Qwen3-0.6B and GGUF local deployment:
  https://huggingface.co/Qwen/Qwen3-0.6B
  https://huggingface.co/Qwen/Qwen3-0.6B-GGUF
- Gemma 4:
  https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/
  https://huggingface.co/blog/gemma4
- Qwen3.5-0.8B:
  https://huggingface.co/Qwen/Qwen3.5-0.8B
- nanochat:
  https://github.com/karpathy/nanochat
- autoresearch:
  https://github.com/karpathy/autoresearch
