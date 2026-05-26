# Starter Repository Skeleton

Copy this structure for a project. It is intentionally minimal and framework
agnostic.

## Structure

```text
configs/
  project.yaml
  train.yaml
  eval.yaml
scripts/
  README.md
```

Suggested project structure after copying:

```text
data/
src/
outputs/
cards/
artifact_manifest.yaml
README.md
```

## Expected Commands

Each project should eventually support commands like:

```bash
python src/prepare_data.py --config configs/project.yaml
python src/train.py --config configs/train.yaml
python src/evaluate.py --config configs/eval.yaml
python src/predict.py --config configs/project.yaml --text "Example input"
```

The exact tools may differ, but the project must document how data preparation,
training, evaluation, and local inference are run.

