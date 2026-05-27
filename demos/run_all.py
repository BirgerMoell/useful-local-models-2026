from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


DEMOS = [
    ("00_next_token_lm", ["--steps", "120"]),
    ("01_tool_router", ["--steps", "160"]),
    ("02_rag_reranker", ["--steps", "180"]),
    ("03_rlvr_arithmetic", ["--steps", "360"]),
    ("04_course_resource_ranker", ["--steps", "260"]),
    ("05_preference_dpo", ["--steps", "120"]),
    ("06_tool_call_sft", ["--steps", "220"]),
    ("07_context_needle", ["--steps", "260"]),
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="auto")
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    for name, default_args in DEMOS:
        script = root / name / "train_eval.py"
        run_args = ["--steps", "40"] if args.quick else default_args
        cmd = [sys.executable, str(script), *run_args, "--device", args.device]
        print("\n==", " ".join(cmd), flush=True)
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
