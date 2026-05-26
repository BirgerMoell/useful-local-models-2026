from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch

sys.path.append(str(Path(__file__).resolve().parents[1]))
from tiny_models import CharTokenizer, TinyCausalLM


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", default="outputs/02_instruction_tuning/checkpoint.pt")
    parser.add_argument("--prompt", default="Instruction: classify: this saved time\nAnswer:")
    parser.add_argument("--max-new-tokens", type=int, default=60)
    args = parser.parse_args()

    checkpoint = Path(args.checkpoint)
    if not checkpoint.exists():
        raise SystemExit(
            f"Missing checkpoint: {checkpoint}\n"
            "Run `python 02_instruction_tuning/train.py` from the examples directory first."
        )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    data = torch.load(checkpoint, map_location=device)
    tokenizer = CharTokenizer([])
    tokenizer.itos = data["vocab"]
    tokenizer.stoi = {token: idx for idx, token in enumerate(tokenizer.itos)}
    model = TinyCausalLM(tokenizer.vocab_size, **data.get("config", {"dim": 112, "heads": 4, "layers": 2})).to(device)
    model.load_state_dict(data["model"])
    ids = torch.tensor([tokenizer.encode(args.prompt, add_bos=True)], device=device)
    out = model.generate(ids, max_new_tokens=args.max_new_tokens, eos_id=tokenizer.eos_id, temperature=0.0)
    print(tokenizer.decode(out[0].tolist()))


if __name__ == "__main__":
    main()

