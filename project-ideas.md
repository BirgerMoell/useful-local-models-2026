# Project Ideas

These are intentionally scoped for one student in a term project. Treat them as
directions for project formulation, not as ready-made assignments. Each student
still needs to choose a concrete dataset, research question, baseline, and
evaluation design.

## Swedish And Nordic Language Tasks

1. Fine-tune a small model to explain Swedish public-sector forms in plain
   language.
2. Train a local model for Swedish grammar feedback and compare to rule-based
   baselines.
3. Adapt a multilingual NER model to Swedish administrative entities.
4. Train a classifier for Swedish support emails or forum questions.
5. Fine-tune an OCR correction model for historical Swedish text.

## Low-Resource And Multilingual Tasks

6. Compare LoRA adaptation across two related low-resource languages.
7. Train a small multilingual instruction model on translated task data and
   evaluate language-specific failures.
8. Study tokenizer fertility and performance for a smaller European language.
9. Train a cross-lingual reranker for Swedish-English document search.
10. Compare English-only vs multilingual training examples for a local model.

## Retrieval And Grounding

11. Train a local reranker for course-document search.
12. Train a citation-selection model for answer grounding.
13. Build a local hallucination detector for answers over a fixed document set.
14. Compare local RAG with a fine-tuned answer model.

## Instruction Tuning And Structured Output

15. Fine-tune a model to extract structured JSON from messy text.
16. Train a local model to rewrite technical text for different audiences.
17. Fine-tune a small model for meeting-note action extraction.
18. Compare SFT and DPO for concise, evidence-grounded answers.

## Verifiable Rewards

19. Use GRPO/RLVR for arithmetic word problems with exact-answer verification.
20. Train a model to solve simple programming tasks using unit-test rewards.
21. Use verifiable rewards for table QA where answers can be checked exactly.
22. Train structured extraction with rewards for valid schema and correct fields.

## Long Context

23. Evaluate whether context extension improves long-document QA in Swedish.
24. Compare long-context prompting against retrieval for multi-document synthesis.
25. Measure lost-in-the-middle behavior before and after long-context adaptation.

## Agentic Tasks

26. Train a small model to emit valid tool calls for a simulated calendar or search
   API.
27. Train a local coding assistant on tiny bug-fix trajectories with unit tests.
28. Train a citation-seeking agent that must choose search, read, and answer
   actions in a local document environment.
29. Compare tool-schema SFT to plain instruction tuning for tool-call validity.

## Safety And Evaluation

30. Train a small multilingual safety classifier for prompt-risk detection.
31. Evaluate whether local instruction tuning weakens refusal behavior.
32. Build a local detector for invalid or unsupported citations.
