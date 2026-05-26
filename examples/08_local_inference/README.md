# 08 Local Inference

Hello-world local checkpoint loading and generation.

Run an instruction-tuning checkpoint first:

```bash
python 02_instruction_tuning/train.py --steps 120
python 08_local_inference/run.py
```

Teaches:

- loading a local checkpoint;
- reconstructing tokenizer and model config;
- generating without an external API;
- final artifact discipline.

