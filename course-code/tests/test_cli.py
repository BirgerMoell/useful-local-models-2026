from pathlib import Path

from lmcourse.cli import main


def test_init_and_validate(tmp_path: Path) -> None:
    project = tmp_path / "demo"
    assert main(["init-project", str(project), "--track", "sft"]) == 0
    assert (project / "agents" / "program.md").exists()
    assert (project / "logs" / "experiments.jsonl").exists()
    assert main(["validate-manifest", str(project / "artifact_manifest.yaml")]) == 0


def test_log_and_summarize(tmp_path: Path) -> None:
    project = tmp_path / "demo"
    assert main(["init-project", str(project)]) == 0
    assert main([
        "log-run",
        str(project),
        "--metric",
        "val_bpb",
        "--value",
        "0.8",
        "--decision",
        "review",
        "--agent-used",
    ]) == 0
    ledger = project / "logs" / "experiments.jsonl"
    assert "val_bpb" in ledger.read_text(encoding="utf-8")
    assert main(["summarize-ledger", str(ledger)]) == 0

