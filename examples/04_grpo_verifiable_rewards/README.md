# 04 GRPO With Verifiable Rewards

Hello-world group-relative policy update with exact-match rewards.

Run:

```bash
python 04_grpo_verifiable_rewards/train.py --steps 40
```

Key mechanics:

- sampling multiple completions per prompt;
- reward functions that can be inspected;
- group-normalized advantages;
- invalid-output penalties.

A compact approximation of the GRPO/RLVR idea, not a production RL trainer.
