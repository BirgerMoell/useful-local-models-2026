# Canvas Module: Theme: Useful Local Models

Suggested Canvas module name:

**Theme: Useful Local Models (Birger Moell)**

Suggested module items:

- Page: **Useful Local Models: Can Small Local Models Be Genuinely Useful?**
- Page or link: **Reading and seminar plan**
- Page or link: **Project ideas and directions**
- Page or link: **Model menu and compute guidance**
- Page or link: **Laptop training demos**
- Page or link: **AI assistance and research integrity**

The text below is the main theme page. It is written in Markdown so it can be
pasted into a Canvas page and then lightly adjusted in the Canvas editor.

---

# Useful Local Models: Can Small Local Models Be Genuinely Useful?

Large language models are often evaluated through remote APIs, leaderboards, and
general chat examples. In this theme we ask a different question:

**Can we make small local models genuinely useful for concrete language
technology tasks?**

The focus is not on building the largest possible model. The focus is on the
research craft behind useful model development: choosing a local use case,
building or adapting data, training a model or model component, comparing
against a meaningful baseline, evaluating on held-out examples, and releasing an
artifact that another person can inspect or run locally.

Projects may use small local language models such as Gemma 4, Qwen3.5, Qwen3,
or other open checkpoints that fit the student's compute budget. A project does
not have to train every stage of a full LLM pipeline. It should make one
research question sharp enough that a student can test it carefully within the
course.

Possible methods include instruction tuning, LoRA or QLoRA adaptation,
continued pretraining, context-length adaptation, preference tuning, trained
classifiers or rerankers, verifiable-reward training, tool-call training, and
small agentic workflows. The method should fit the task. A narrow classifier,
reranker, or adapter is often a better project than an overambitious chat model.

AI agents and coding assistants may be used for implementation, debugging, and
experiment support. Students must still understand, verify, and disclose how
they used these tools. Claims in the final paper must be supported by baselines,
held-out evaluation, saved outputs, and human analysis.

## What Counts As A Good Project?

A good project in this theme has:

- a specific language technology task;
- a reason local execution matters;
- a baseline that is hard enough to be meaningful;
- a model or component whose parameters are trained or adapted;
- a held-out evaluation set;
- an error analysis;
- a local runnable or inspectable artifact;
- clear limits on what the result shows.

The examples in the course repository are starting points, not finished project
topics. Each student formulates an individual research question, chooses a
dataset or data construction method, and designs an evaluation.

## Example Project Directions

These are directions for project scoping, not ready-made assignments.

- Can a small local model extract useful structured information from Swedish or
  multilingual text better than a rule-based baseline?
- Does instruction tuning improve a local model on a narrow domain task, or does
  retrieval plus prompting work just as well?
- Can a local reranker improve search quality for course documents, public
  reports, legal text, medical information, or cultural heritage material?
- Can a small model learn reliable tool calls for a constrained local workflow?
- Does context extension improve performance on tasks that actually require
  long-distance evidence?
- Can preference tuning reduce overclaiming or improve answer usefulness in a
  specific setting?
- Can verifiable rewards improve a model on tasks with objective checks, such as
  JSON validity, unit tests, arithmetic, or exact extraction?
- What does a model card, dataset card, and artifact manifest need to say for a
  local model to be scientifically inspectable?

## Seminar 1: Open Training Pipelines And Artifacts

This seminar looks at what makes model training scientifically inspectable. We
discuss open models, open datasets, model cards, data documentation, and the
difference between a downloadable model and an auditable research artifact.

Assigned papers:

- Groeneveld et al. 2024. **OLMo: Accelerating the Science of Language Models**.
  https://arxiv.org/abs/2402.00838  
  Presenter: TBD
- Soldaini et al. 2024. **Dolma: An Open Corpus of Three Trillion Tokens for
  Language Model Pretraining Research**.
  https://arxiv.org/abs/2402.00159  
  Presenter: TBD
- Mitchell et al. 2019. **Model Cards for Model Reporting**.
  https://arxiv.org/abs/1810.03993  
  Presenter: TBD

Discussion questions:

- Which artifacts are needed to audit a model-training claim?
- What does "open" mean beyond making weights downloadable?
- What kind of data documentation is realistic in a student project?
- How should students check for contamination, leakage, and overclaiming?

## Seminar 2: Fine-Tuning Small Local Models

This seminar focuses on adapting models with limited compute. We discuss
supervised fine-tuning, parameter-efficient adaptation, instruction tuning, and
what students should compare against before claiming that training helped.

Assigned papers:

- Hu et al. 2021. **LoRA: Low-Rank Adaptation of Large Language Models**.
  https://arxiv.org/abs/2106.09685  
  Presenter: TBD
- Dettmers et al. 2023. **QLoRA: Efficient Finetuning of Quantized LLMs**.
  https://arxiv.org/abs/2305.14314  
  Presenter: TBD
- Ouyang et al. 2022. **Training Language Models to Follow Instructions with
  Human Feedback**.
  https://arxiv.org/abs/2203.02155  
  Presenter: TBD

Discussion questions:

- What is actually trained in LoRA or QLoRA?
- When is instruction tuning the right method?
- When is a classifier, reranker, or retrieval component a better local model?
- What should the baseline be for a small-model adaptation project?

## Seminar 3: Advanced Techniques And Agent-Assisted Research

This seminar looks at methods that are powerful but easy to overclaim:
preference tuning, verifiable rewards, context extension, and agent-assisted
experimentation. The focus is on when these methods make sense and how to
evaluate them responsibly.

Assigned papers:

- Rafailov et al. 2023. **Direct Preference Optimization: Your Language Model is
  Secretly a Reward Model**.
  https://arxiv.org/abs/2305.18290  
  Presenter: TBD
- Shao et al. 2024. **DeepSeekMath: Pushing the Limits of Mathematical Reasoning
  in Open Language Models**.
  https://arxiv.org/abs/2402.03300  
  Presenter: TBD
- Peng et al. 2023. **YaRN: Efficient Context Window Extension of Large Language
  Models**.
  https://arxiv.org/abs/2309.00071  
  Presenter: TBD

Discussion questions:

- What makes a reward verifiable?
- Why should reinforcement-style methods be restricted to tasks with clear
  automatic checks?
- How can we test whether a model really uses long context?
- What can an AI agent help with, and what must the student verify manually?

## Additional Reading

Students should use the additional reading list to find work close to their own
task, language, method, or evaluation problem.

Open training and artifacts:

- Birger Moell. 2026. **The 2026 Fully Open LLM Training Guide**.
  https://birgermoell.github.io/openeurollm-open-llm-guide/docs/fully-open-llm-guide-2026.pdf
- Karpathy. **nanochat**. https://github.com/karpathy/nanochat
- Karpathy. **autoresearch**. https://github.com/karpathy/autoresearch
- Hugging Face. **Model cards**. https://huggingface.co/docs/hub/model-cards
- Hugging Face. **Dataset cards**.
  https://huggingface.co/docs/datasets/dataset_card

Fine-tuning and local adaptation:

- Hugging Face. **PEFT documentation**. https://huggingface.co/docs/peft
- Hugging Face. **TRL SFTTrainer**.
  https://huggingface.co/docs/trl/sft_trainer
- Hugging Face. **TRL DPOTrainer**.
  https://huggingface.co/docs/trl/dpo_trainer
- Hugging Face. **TRL GRPOTrainer**.
  https://huggingface.co/docs/trl/grpo_trainer
- Wang et al. 2022. **Self-Instruct: Aligning Language Models with
  Self-Generated Instructions**. https://arxiv.org/abs/2212.10560
- Wei et al. 2021. **Finetuned Language Models Are Zero-Shot Learners**.
  https://arxiv.org/abs/2109.01652

Local model families and deployment:

- Qwen model collection. https://huggingface.co/Qwen
- Gemma model documentation. https://ai.google.dev/gemma
- llama.cpp GGUF documentation.
  https://huggingface.co/docs/hub/en/gguf-llamacpp
- Ollama Modelfile documentation. https://docs.ollama.com/modelfile
- MLX-LM. https://github.com/ml-explore/mlx-lm

Context and long-context evaluation:

- Chen et al. 2023. **Extending Context Window of Large Language Models via
  Positional Interpolation**. https://arxiv.org/abs/2306.15595
- Ding et al. 2024. **LongRoPE: Extending LLM Context Window Beyond 2 Million
  Tokens**. https://arxiv.org/abs/2402.13753
- Hsieh et al. 2024. **RULER: What's the Real Context Size of Your
  Long-Context Language Models?** https://arxiv.org/abs/2404.06654

Agents, tools, and retrieval:

- Schick et al. 2023. **Toolformer: Language Models Can Teach Themselves to Use
  Tools**. https://arxiv.org/abs/2302.04761
- Yao et al. 2022. **ReAct: Synergizing Reasoning and Acting in Language
  Models**. https://arxiv.org/abs/2210.03629
- Khattab and Zaharia. 2020. **ColBERT: Efficient and Effective Passage Search
  via Contextualized Late Interaction**. https://arxiv.org/abs/2004.12832
- Nogueira et al. 2020. **Document Ranking with a Pretrained Sequence-to-Sequence
  Model**. https://arxiv.org/abs/2003.06713
- Reimers and Gurevych. 2019. **Sentence-BERT: Sentence Embeddings using
  Siamese BERT-Networks**. https://arxiv.org/abs/1908.10084

## Technical Expectations

Each project should produce a small but inspectable technical package. Depending
on the project, this may be a trained adapter, checkpoint, reranker, classifier,
GGUF model, MLX model, ONNX export, or reproducible training script.

The final artifact should include:

- a README with local run instructions;
- training and evaluation configs;
- data documentation;
- saved metrics;
- representative outputs;
- model card or artifact card;
- limitations and known failure cases.

Students do not need to make the largest possible model run locally. They need
to show, with evidence, whether a small local model or trained component became
useful for a specific task.

## Course Repository

The theme resources, tiny training examples, laptop demos, assignment guidance,
and templates are collected here:

https://birgermoell.github.io/useful-local-models-2026/

Students may use these materials for orientation and implementation practice.
Their submitted project should still have its own research question, dataset,
method choice, and evaluation design.
