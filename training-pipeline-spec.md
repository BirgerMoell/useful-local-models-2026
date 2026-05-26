# Training Pipeline Specification

Every project must produce an auditable training pipeline. This does not require
large-scale infrastructure, but it does require careful records.

## Required Stages

### 1. Project Charter

Record:

- research question;
- task;
- language(s);
- intended local use;
- target hardware;
- model family;
- expected output artifact.

### 2. Data Source Registry

For every data source, record:

- source name;
- URL or storage path;
- snapshot date;
- acquisition method;
- license or terms;
- language/domain;
- approximate size;
- known risks;
- redistribution status;
- preprocessing performed.

### 3. Splits

Every empirical project must define train/dev/test splits.

Requirements:

- fixed random seed or deterministic split rule;
- no duplicated examples across splits;
- no exact benchmark examples in training data where benchmark evaluation is used;
- explanation of any manual filtering.

### 4. Baseline

The baseline should be meaningful and cheap.

Examples:

- majority class;
- logistic regression;
- BM25;
- frozen embeddings;
- base model prompting;
- zero-shot or few-shot model response;
- previous small model without adaptation.

### 5. Training

Training record must include:

- base model and revision;
- tokenizer;
- training method;
- optimizer;
- learning rate;
- batch size and gradient accumulation;
- max sequence length;
- epochs or steps;
- LoRA/QLoRA parameters if used;
- random seed;
- hardware;
- wall-clock time;
- checkpoint path;
- failure or restart notes.

### 6. Evaluation

Evaluation must include:

- metric definitions;
- held-out data;
- baseline comparison;
- parse failure rate for generated outputs;
- error analysis;
- significance testing where appropriate;
- cost or latency where relevant;
- local inference setting.

### 7. Local Release

The final artifact package should include:

- model or adapter;
- local inference command;
- model card;
- dataset card or data statement;
- artifact manifest;
- evaluation outputs;
- known limitations.

## Recommended File Structure

```text
project/
  README.md
  configs/
    project.yaml
    train.yaml
    eval.yaml
  data/
    README.md
    source_registry.csv
    splits/
  src/
    prepare_data.py
    train.py
    evaluate.py
    export_local.py
  outputs/
    checkpoints/
    eval/
    logs/
  cards/
    model_card.md
    dataset_card.md
  artifact_manifest.yaml
```

## Minimum Training Config Fields

```yaml
base_model: Qwen/Qwen3-0.6B
base_model_revision: main
training_method: qlora_sft
task: instruction_following
language: sv
max_seq_length: 2048
learning_rate: 0.0002
batch_size_per_device: 2
gradient_accumulation_steps: 8
epochs: 3
seed: 13
lora:
  r: 16
  alpha: 32
  dropout: 0.05
  target_modules: ["q_proj", "k_proj", "v_proj", "o_proj"]
quantization:
  load_in_4bit: true
  quant_type: nf4
evaluation:
  primary_metric: exact_match
  baseline: base_model_prompting
local_release:
  format: peft_adapter
  target_runtime: transformers
```

Students should adapt this. They should not copy it blindly.

