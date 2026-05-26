from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = PACKAGE_ROOT / "templates"

REQUIRED_MANIFEST_KEYS = [
    "project_name",
    "research_question",
    "task",
    "base_model",
    "trained_artifact",
    "data",
    "training",
    "evaluation",
    "local_run",
    "documentation",
]


def now_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def read_text_template(name: str) -> str:
    return (TEMPLATE_DIR / name).read_text(encoding="utf-8")


def write_if_missing(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def cmd_init_project(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    root.mkdir(parents=True, exist_ok=True)

    for dirname in ["agents", "cards", "configs", "data", "logs", "outputs", "src"]:
        (root / dirname).mkdir(exist_ok=True)

    replacements = {
        "{{PROJECT_NAME}}": root.name,
        "{{TRACK}}": args.track,
        "{{DATE}}": datetime.now().date().isoformat(),
    }

    def render(template_name: str) -> str:
        text = read_text_template(template_name)
        for key, value in replacements.items():
            text = text.replace(key, value)
        return text

    write_if_missing(root / "README.md", render("project_README.md"))
    write_if_missing(root / "agents" / "program.md", render("agent_program.md"))
    write_if_missing(root / "cards" / "model_card.md", render("model_card.md"))
    write_if_missing(root / "cards" / "dataset_card.md", render("dataset_card.md"))
    write_if_missing(root / "configs" / "project.yaml", render("project.yaml"))
    write_if_missing(root / "configs" / "train.yaml", render("train.yaml"))
    write_if_missing(root / "configs" / "eval.yaml", render("eval.yaml"))
    write_if_missing(root / "artifact_manifest.yaml", render("artifact_manifest.yaml"))
    write_if_missing(root / "src" / "README.md", "# Source Code\n\nPut project scripts here.\n")
    write_if_missing(root / "logs" / "experiments.jsonl", "")

    registry = root / "data" / "source_registry.csv"
    if not registry.exists():
        with registry.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "source_name",
                "url_or_path",
                "snapshot_date",
                "license",
                "language",
                "domain",
                "redistribution",
                "known_risks",
            ])

    print(f"Initialized project at {root}")
    return 0


def shallow_manifest_keys(path: Path) -> set[str]:
    keys: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" ") and ":" in line:
            keys.add(line.split(":", 1)[0].strip())
    return keys


def cmd_validate_manifest(args: argparse.Namespace) -> int:
    path = Path(args.manifest)
    if not path.exists():
        print(f"Missing manifest: {path}")
        return 2

    keys = shallow_manifest_keys(path)
    missing = [key for key in REQUIRED_MANIFEST_KEYS if key not in keys]
    if missing:
        print("Manifest is missing required top-level keys:")
        for key in missing:
            print(f"- {key}")
        return 1

    print("Manifest has the required top-level keys.")
    return 0


def cmd_log_run(args: argparse.Namespace) -> int:
    project = Path(args.project)
    ledger = project / "logs" / "experiments.jsonl"
    ledger.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "run_id": args.run_id or now_id(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "hypothesis": args.hypothesis,
        "metric": args.metric,
        "value": args.value,
        "decision": args.decision,
        "agent_used": args.agent_used,
        "note": args.note,
    }
    with ledger.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"Logged run to {ledger}")
    return 0


def cmd_summarize_ledger(args: argparse.Namespace) -> int:
    ledger = Path(args.ledger)
    if not ledger.exists():
        print(f"Missing ledger: {ledger}")
        return 2

    records = []
    for line in ledger.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))

    print(f"Runs: {len(records)}")
    if not records:
        return 0

    by_metric: dict[str, list[float]] = {}
    for record in records:
        metric = record.get("metric") or "unknown"
        value = record.get("value")
        if isinstance(value, (int, float)):
            by_metric.setdefault(metric, []).append(float(value))

    for metric, values in by_metric.items():
        print(f"{metric}: best={min(values):.6g}, last={values[-1]:.6g}, n={len(values)}")

    decisions: dict[str, int] = {}
    for record in records:
        decision = record.get("decision") or "unspecified"
        decisions[decision] = decisions.get(decision, 0) + 1
    print("Decisions:")
    for decision, count in sorted(decisions.items()):
        print(f"- {decision}: {count}")
    return 0


def cmd_copy_template(args: argparse.Namespace) -> int:
    destination = Path(args.destination)
    template = TEMPLATE_DIR / args.template
    if not template.exists():
        print(f"Unknown template: {args.template}")
        return 2
    shutil.copyfile(template, destination)
    print(f"Copied {template} to {destination}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="lmcourse")
    sub = parser.add_subparsers(dest="command", required=True)

    init_project = sub.add_parser("init-project", help="Create a student project scaffold")
    init_project.add_argument("path")
    init_project.add_argument("--track", default="sft")
    init_project.set_defaults(func=cmd_init_project)

    validate = sub.add_parser("validate-manifest", help="Check required manifest keys")
    validate.add_argument("manifest")
    validate.set_defaults(func=cmd_validate_manifest)

    log_run = sub.add_parser("log-run", help="Append a run to logs/experiments.jsonl")
    log_run.add_argument("project")
    log_run.add_argument("--run-id")
    log_run.add_argument("--hypothesis", default="")
    log_run.add_argument("--metric", required=True)
    log_run.add_argument("--value", type=float, required=True)
    log_run.add_argument("--decision", choices=["keep", "reject", "review", "rerun"], default="review")
    log_run.add_argument("--agent-used", action="store_true")
    log_run.add_argument("--note", default="")
    log_run.set_defaults(func=cmd_log_run)

    summarize = sub.add_parser("summarize-ledger", help="Summarize a JSONL experiment ledger")
    summarize.add_argument("ledger")
    summarize.set_defaults(func=cmd_summarize_ledger)

    copy_template = sub.add_parser("copy-template", help="Copy a named template")
    copy_template.add_argument("template")
    copy_template.add_argument("destination")
    copy_template.set_defaults(func=cmd_copy_template)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
