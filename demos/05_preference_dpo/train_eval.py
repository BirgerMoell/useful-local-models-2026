from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path

import torch
import torch.nn.functional as F

sys.path.append(str(Path(__file__).resolve().parents[2] / "examples"))
sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import choose_device, ensure_dir, save_json, set_seed
from tiny_models import CharTokenizer, TinyCausalLM


TRAIN_PREFS = [
    (
        "Write a limitation for a local model that routes training commands.",
        "Limitation: it only covers the tool schemas seen in training and should fall back to human review on unfamiliar commands.",
        "This model is always reliable and can safely execute any command without checks.",
    ),
    (
        "Write a model-card risk for a small local medical summarizer.",
        "Risk: it may omit clinically important details, so summaries need source links and human review before use.",
        "Risk: none, because local models do not make mistakes when data stays private.",
    ),
    (
        "Explain why a reranker evaluation needs held-out queries.",
        "Held-out queries show whether the reranker learned relevance patterns instead of memorizing the training pairs.",
        "Held-out queries are optional if the training loss looks smooth.",
    ),
    (
        "Write a concise artifact note for a context-extension experiment.",
        "The release must report the target context length, memory use, and tests that require distant evidence.",
        "The release can claim long context as soon as the sequence length flag is larger.",
    ),
    (
        "Give a useful failure note for an instruction-tuned local assistant.",
        "Failure: the model follows familiar templates but gives invalid JSON on unseen tool arguments.",
        "Failure: the model is creative, which means the evaluation should be ignored.",
    ),
    (
        "State a privacy benefit without overclaiming.",
        "Running locally can reduce data sharing, but logs, prompts, and checkpoints still need access controls.",
        "Running locally guarantees privacy in every possible deployment.",
    ),
    (
        "Write an evaluation claim for a tiny tool-call model.",
        "On the held-out split, the model selects the correct tool in 18 of 20 cases and emits valid JSON in 19 of 20.",
        "The model feels better after training, so it is ready to ship.",
    ),
    (
        "Describe what agent-written code needs before it counts as evidence.",
        "Agent-written changes need reviewed diffs, recorded prompts, and tests that support the reported claim.",
        "Agent-written code counts as evidence because the agent sounded confident.",
    ),
    (
        "Write a reward-design note for RLVR.",
        "The reward should be computed by a transparent verifier, such as unit tests, exact arithmetic, or schema checks.",
        "The reward should be whatever makes the generated answer longer.",
    ),
    (
        "Explain why a base-model baseline matters.",
        "A baseline shows whether training improved the task beyond prompting, rules, or retrieval alone.",
        "A baseline is unnecessary when the technique is modern.",
    ),
]


TEST_PREFS = [
    (
        "Write a deployment limitation for a Qwen-sized local adapter.",
        "Limitation: results depend on quantization, prompt template, memory budget, and the exact adapter checkpoint.",
        "There are no deployment limitations once the adapter loads.",
    ),
    (
        "Explain what a useful local model report should include.",
        "The report should include the task, data split, baseline, training change, held-out metrics, errors, and run command.",
        "The report should mostly describe why local models are exciting.",
    ),
    (
        "Give a safe claim for a model trained on synthetic data.",
        "Synthetic data can test the training loop, but real deployment claims need data closer to the target use case.",
        "Synthetic data proves the model will work on real users.",
    ),
    (
        "Write a note about failed runs.",
        "Failed runs are useful when they record the hypothesis, config, metric movement, and next decision.",
        "Failed runs should be deleted from the project history.",
    ),
]


def completion_logprob(model: TinyCausalLM, tokenizer: CharTokenizer, prompt: str, completion: str, device: torch.device) -> torch.Tensor:
    prompt_ids = tokenizer.encode(prompt, add_bos=True)
    completion_ids = tokenizer.encode(completion, add_eos=True)
    full = prompt_ids + completion_ids
    x = torch.tensor([full[:-1]], device=device)
    y = torch.tensor([full[1:]], device=device)
    logits = model(x)
    logp = F.log_softmax(logits, dim=-1).gather(-1, y[..., None]).squeeze(-1)[0]
    completion_start = len(prompt_ids) - 1
    return logp[completion_start:].mean()


@torch.no_grad()
def evaluate(model: TinyCausalLM, tokenizer: CharTokenizer, rows: list[tuple[str, str, str]], device: torch.device) -> dict:
    model.eval()
    examples = []
    correct = 0
    for prompt, chosen, rejected in rows:
        chosen_logp = completion_logprob(model, tokenizer, prompt, chosen, device).item()
        rejected_logp = completion_logprob(model, tokenizer, prompt, rejected, device).item()
        margin = chosen_logp - rejected_logp
        correct += int(margin > 0)
        examples.append(
            {
                "prompt": prompt,
                "chosen_logp": round(chosen_logp, 4),
                "rejected_logp": round(rejected_logp, 4),
                "margin": round(margin, 4),
                "preferred": "chosen" if margin > 0 else "rejected",
            }
        )
    model.train()
    return {"preference_accuracy": correct / len(rows), "examples": examples}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--beta", type=float, default=0.2)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--out", default="outputs/demos/05_preference_dpo")
    args = parser.parse_args()

    set_seed(106)
    device = choose_device(args.device)
    texts = [item for row in TRAIN_PREFS + TEST_PREFS for item in row]
    tokenizer = CharTokenizer(texts)
    config = {"dim": 96, "heads": 4, "layers": 1}
    policy = TinyCausalLM(tokenizer.vocab_size, **config).to(device)
    reference = copy.deepcopy(policy).to(device)
    for param in reference.parameters():
        param.requires_grad_(False)
    opt = torch.optim.AdamW(policy.parameters(), lr=1.5e-3)
    initial = evaluate(policy, tokenizer, TEST_PREFS, device)

    for step in range(1, args.steps + 1):
        losses = []
        for prompt, chosen, rejected in TRAIN_PREFS:
            pi_chosen = completion_logprob(policy, tokenizer, prompt, chosen, device)
            pi_rejected = completion_logprob(policy, tokenizer, prompt, rejected, device)
            with torch.no_grad():
                ref_chosen = completion_logprob(reference, tokenizer, prompt, chosen, device)
                ref_rejected = completion_logprob(reference, tokenizer, prompt, rejected, device)
            pi_margin = pi_chosen - pi_rejected
            ref_margin = ref_chosen - ref_rejected
            losses.append(-F.logsigmoid(args.beta * (pi_margin - ref_margin)))
        loss = torch.stack(losses).mean()
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if step == 1 or step % 40 == 0:
            train_eval = evaluate(policy, tokenizer, TRAIN_PREFS, device)
            print(f"step {step:04d} dpo_loss {loss.item():.4f} train_pref_acc {train_eval['preference_accuracy']:.3f}")

    final = evaluate(policy, tokenizer, TEST_PREFS, device)
    summary = {
        "demo": "preference_dpo",
        "data": "synthetic chosen/rejected pairs about local-model project reports",
        "device": str(device),
        "steps": args.steps,
        "beta": args.beta,
        "initial_eval": initial,
        "final_eval": final,
        "preference_accuracy_delta": final["preference_accuracy"] - initial["preference_accuracy"],
    }
    out = ensure_dir(args.out)
    torch.save({"model": policy.state_dict(), "vocab": tokenizer.itos, "config": config}, out / "checkpoint.pt")
    save_json(out / "summary.json", summary)
    print(summary)


if __name__ == "__main__":
    main()
