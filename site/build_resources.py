from __future__ import annotations

import builtins
import html
import io
import keyword
import re
import tokenize
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "resources"

DOCS = {
    "student-project-brief": ROOT / "student-project-brief.md",
    "examples": ROOT / "examples" / "README.md",
    "laptop-demos": ROOT / "demos" / "README.md",
    "laptop-demo-results": ROOT / "demos" / "verified-results.md",
    "course-code": ROOT / "course-code" / "README.md",
    "local-deployment-guide": ROOT / "local-deployment-guide.md",
    "project-tracks": ROOT / "project-tracks.md",
    "canvas-course-setup": ROOT / "canvas-course-setup.md",
    "canvas-theme-module-useful-local-models": ROOT / "canvas-theme-module-useful-local-models.md",
    "teacher-overview": ROOT / "teacher-overview.md",
    "teacher-start-checklist": ROOT / "teacher-start-checklist.md",
    "milestones-and-schedule": ROOT / "milestones-and-schedule.md",
    "reading-and-seminar-plan": ROOT / "reading-and-seminar-plan.md",
    "rubric": ROOT / "rubric.md",
    "project-format": ROOT / "project-format.md",
    "ai-assistance-policy": ROOT / "ai-assistance-policy.md",
    "modern-tooling-map": ROOT / "modern-tooling-map.md",
    "model-menu-and-compute": ROOT / "model-menu-and-compute.md",
    "project-ideas": ROOT / "project-ideas.md",
    "project-intake-form": ROOT / "templates" / "project-intake-form.md",
    "training-pipeline-spec": ROOT / "training-pipeline-spec.md",
    "advanced-techniques-guide": ROOT / "advanced-techniques-guide.md",
    "worked-systems": ROOT / "nanochat-autoresearch-integration.md",
    "studium-task-overview": ROOT / "assignment-pages" / "studium-task-overview.md",
    "studium-philosophy-assignment": ROOT / "assignment-pages" / "studium-philosophy-assignment.md",
    "studium-theme-description": ROOT / "assignment-pages" / "studium-theme-description.md",
    "studium-literature-seminars": ROOT / "assignment-pages" / "studium-literature-seminars.md",
    "studium-proposal-assignment": ROOT / "assignment-pages" / "studium-proposal-assignment.md",
    "studium-popular-science-abstract": ROOT / "assignment-pages" / "studium-popular-science-abstract.md",
    "studium-proposal-presentation": ROOT / "assignment-pages" / "studium-proposal-presentation.md",
    "studium-progress-seminars": ROOT / "assignment-pages" / "studium-progress-seminars.md",
    "studium-first-report": ROOT / "assignment-pages" / "studium-first-report.md",
    "studium-peer-review-instructions": ROOT / "assignment-pages" / "studium-peer-review-instructions.md",
    "studium-project-presentation": ROOT / "assignment-pages" / "studium-project-presentation.md",
    "studium-final-report": ROOT / "assignment-pages" / "studium-final-report.md",
}


EXAMPLE_AREAS = [
    {
        "slug": "pretraining",
        "title": "01 Pretraining",
        "directory": "01_pretraining",
        "script": "examples/01_pretraining/train.py",
        "command": "python 01_pretraining/train.py --steps 80",
        "technique": "Next-token language-model training",
        "why": "Pretraining is the base objective for decoder-only language models: make text into tokens, predict the next token, update weights, save a checkpoint, then inspect a sample.",
        "look_at": ["TEXTS as the training corpus", "make_lm_batch for x/y next-token pairs", "cross_entropy_loss(model(x), y)", "torch.save plus summary.json"],
        "concepts": [
            ("TEXTS", "A minimal training corpus represented as plain strings. Keeping the corpus visible makes every token inspectable; larger runs need a documented dataset with train/dev/test splits."),
            ("make_lm_batch", "Builds next-token examples by slicing token_ids into x and y. x is the context the model sees; y is the same text shifted one token to the right, the token the model should predict at each position."),
            ("cross_entropy_loss(model(x), y)", "model(x) returns logits: one score for every possible next token. Cross entropy turns those scores into probabilities and penalizes the model when it assigns low probability to the correct next token in y."),
            ("torch.save and summary.json", "The checkpoint stores the runnable model state. summary.json stores human-readable evidence such as final loss and samples, so a result can be inspected without loading PyTorch."),
        ],
        "resources": [
            ("Attention Is All You Need", "https://arxiv.org/abs/1706.03762", "Transformer architecture and attention as the computational substrate."),
            ("GPT-2 paper and code", "https://github.com/openai/gpt-2", "A canonical decoder-only next-token model release with model-card caveats."),
            ("nanochat", "https://github.com/karpathy/nanochat", "Readable full-stack local training lifecycle for a larger reference implementation."),
        ],
    },
    {
        "slug": "instruction-tuning",
        "title": "02 Instruction Tuning",
        "directory": "02_instruction_tuning",
        "script": "examples/02_instruction_tuning/train.py",
        "command": "python 02_instruction_tuning/train.py --steps 120",
        "technique": "Supervised fine-tuning",
        "why": "Instruction tuning turns a base model into a task-following model. For useful local models, this is often the first practical adaptation step before preferences, rewards, or deployment.",
        "look_at": ["format_example defines the prompt/answer contract", "PAIRS is the demonstration dataset", "SFT is still next-token prediction", "probes test behavior after training"],
        "concepts": [
            ("Prompt format", "The model learns the literal pattern Instruction: ... Answer: ... . Small formatting choices become part of the learned behavior."),
            ("Demonstrations", "PAIRS are supervised examples. They do not merely label the task; they show the output style the model should imitate."),
            ("SFT objective", "Supervised fine-tuning still uses next-token cross entropy. The difference is the data: examples are formatted as task demonstrations."),
            ("Probes", "Held-out prompts give a quick behavior check. They are not a full evaluation, but they catch obvious failures before larger runs."),
        ],
        "resources": [
            ("InstructGPT", "https://arxiv.org/abs/2203.02155", "Shows supervised demonstrations as the first stage of instruction-following alignment."),
            ("LoRA", "https://arxiv.org/abs/2106.09685", "A common parameter-efficient adaptation method for real model runs."),
            ("Hugging Face TRL SFT", "https://huggingface.co/docs/trl/sft_trainer", "Production-grade SFT trainer and dataset formatting reference."),
            ("Hugging Face PEFT LoRA", "https://huggingface.co/docs/peft/en/package_reference/lora", "Practical LoRA configuration knobs for adapters."),
        ],
    },
    {
        "slug": "preference-dpo",
        "title": "03 Preference DPO",
        "directory": "03_preference_dpo",
        "script": "examples/03_preference_dpo/train.py",
        "command": "python 03_preference_dpo/train.py --steps 80",
        "technique": "Direct Preference Optimization",
        "why": "Preference tuning optimizes relative quality when several answers may be plausible. DPO compares chosen and rejected completions directly, avoiding a separately trained reward model.",
        "look_at": ["PREFS as chosen/rejected pairs", "frozen reference model", "logprob_completion over answer tokens", "the DPO margin and logsigmoid loss"],
        "concepts": [
            ("Chosen and rejected", "Preference data says one answer is better than another for the same prompt. It is about relative quality, not a single gold string."),
            ("Reference model", "The frozen copy anchors the update so the policy learns preferences without drifting only by making every chosen answer more likely."),
            ("Log probability", "DPO compares how much probability the model assigns to complete chosen and rejected answers, token by token."),
            ("DPO margin", "The loss rewards the policy when its chosen-vs-rejected gap is better than the reference model's gap."),
        ],
        "resources": [
            ("DPO paper", "https://arxiv.org/abs/2305.18290", "Core derivation of preference optimization as a simple classification-style loss."),
            ("Hugging Face TRL DPO", "https://huggingface.co/docs/trl/dpo_trainer", "Trainer API and dataset schema for real DPO runs."),
            ("Anthropic HH-RLHF dataset", "https://huggingface.co/datasets/Anthropic/hh-rlhf", "Classic preference-style data for discussing chosen/rejected labels and their limits."),
        ],
    },
    {
        "slug": "grpo-verifiable-rewards",
        "title": "04 GRPO With Verifiable Rewards",
        "directory": "04_grpo_verifiable_rewards",
        "script": "examples/04_grpo_verifiable_rewards/train.py",
        "command": "python 04_grpo_verifiable_rewards/train.py --steps 40",
        "technique": "Group-relative policy updates and RLVR",
        "why": "Verifiable rewards matter because claims can be checked. A GRPO-style update samples multiple answers, scores them with a transparent function, and turns relative success into a learning signal.",
        "look_at": ["reward_fn as the verifier", "group-size completions per prompt", "normalized group advantages", "loss from logprobs times advantages"],
        "concepts": [
            ("Verifier", "reward_fn is a small automatic judge. It makes the reward inspectable, which is why arithmetic, unit tests, and schema checks are useful domains."),
            ("Group sampling", "The model samples several completions for one prompt. The update learns from which samples were better within that local group."),
            ("Advantage", "A reward above the group mean becomes positive pressure; a reward below the group mean becomes negative pressure."),
            ("Policy update", "Multiplying logprobs by advantages increases the probability of rewarded samples and decreases the probability of weak samples."),
        ],
        "resources": [
            ("DeepSeekMath", "https://arxiv.org/abs/2402.03300", "Introduces GRPO in an open mathematical-reasoning model pipeline."),
            ("DeepSeek-R1", "https://arxiv.org/abs/2501.12948", "Important modern reference for reasoning with reinforcement learning and verifiable tasks."),
            ("Hugging Face TRL GRPO", "https://huggingface.co/docs/trl/grpo_trainer", "Practical trainer documentation for GRPO-style experiments."),
        ],
    },
    {
        "slug": "context-extension",
        "title": "05 Context Extension",
        "directory": "05_context_extension",
        "script": "examples/05_context_extension/train.py",
        "command": "python 05_context_extension/train.py --steps 120",
        "technique": "Long-context adaptation",
        "why": "Long context is easy to claim and hard to prove. The tiny run separates short-context training, longer-context adaptation, RoPE scaling, and evaluation at the target length.",
        "look_at": ["short-len vs long-len phases", "rope_scale passed into the model", "eval_loss at short and long lengths", "summary warns against overclaiming"],
        "concepts": [
            ("Context length", "The number of tokens the model can condition on at once. Longer windows are useful only if the model actually uses far-away evidence."),
            ("RoPE scaling", "A position-embedding adjustment that changes how the model represents token positions beyond the original training length."),
            ("Adaptation phase", "A two-phase adaptation first trains short, then continues with longer sequences and a RoPE scale."),
            ("Long-context evaluation", "Loss at longer length is only a smoke test. Real claims need tasks that require evidence from distant positions."),
        ],
        "resources": [
            ("RoFormer / RoPE", "https://arxiv.org/abs/2104.09864", "The rotary position embedding idea many local LLMs use."),
            ("Position Interpolation", "https://arxiv.org/abs/2306.15595", "A central method for extending RoPE-based context windows with limited fine-tuning."),
            ("YaRN", "https://arxiv.org/abs/2309.00071", "Widely used follow-up for efficient context extension."),
            ("RULER", "https://arxiv.org/abs/2404.06654", "Evaluation warning: nominal context length is not the same as effective context length."),
        ],
    },
    {
        "slug": "tool-use-sft",
        "title": "06 Tool-Use SFT",
        "directory": "06_tool_use_sft",
        "script": "examples/06_tool_use_sft/train.py",
        "command": "python 06_tool_use_sft/train.py --steps 120",
        "technique": "Structured tool-call training",
        "why": "A small model can be useful when its job is narrow and structured. Tool-use SFT focuses on valid calls, schema discipline, and local task routing rather than open-ended chat quality.",
        "look_at": ["EXAMPLES as user intent to JSON calls", "format_example as the schema contract", "complete for local generation", "JSON validity as an evaluation target"],
        "concepts": [
            ("Tool call", "The desired output is structured data, not prose. The model's job is to choose the right tool name and arguments."),
            ("Schema contract", "The format is part of the task. If the output is invalid JSON, the agent cannot reliably use it."),
            ("Constrained behavior", "Small local models can be valuable when the output space is narrow and evaluation is crisp."),
            ("Validity metric", "A system can score parse rate, schema pass rate, and task success instead of only text quality."),
        ],
        "resources": [
            ("Toolformer", "https://arxiv.org/abs/2302.04761", "Shows how language models can learn when and how to call external tools."),
            ("ReAct", "https://arxiv.org/abs/2210.03629", "Connects reasoning traces with actions in external environments."),
            ("Berkeley Function-Calling Leaderboard", "https://gorilla.cs.berkeley.edu/leaderboard.html", "Useful benchmark family for thinking about function-call correctness."),
        ],
    },
    {
        "slug": "reranker",
        "title": "07 Reranker",
        "directory": "07_reranker",
        "script": "examples/07_reranker/train.py",
        "command": "python 07_reranker/train.py --steps 120",
        "technique": "Local retrieval/reranking",
        "why": "Not every useful local model should generate text. Rerankers are small, measurable, and useful in RAG/search pipelines where the model only needs to score query-document relevance.",
        "look_at": ["PAIRS as query/document/label triples", "featurize as a tiny stand-in for encoders", "TinyReranker scoring query-doc pairs", "scores saved for inspection"],
        "concepts": [
            ("Query/document pair", "The model sees a query and one candidate document, then predicts whether the document is relevant."),
            ("Feature representation", "The compact featurizer uses character counts; real systems use encoder embeddings or cross-encoder representations."),
            ("Binary relevance loss", "The reranker uses a classification objective, showing that useful local models do not always need language generation."),
            ("Ranking evidence", "Saved scores make it possible to inspect which documents were pushed up or down and whether the behavior matches labels."),
        ],
        "resources": [
            ("ColBERT", "https://arxiv.org/abs/2004.12832", "Efficient neural retrieval with late interaction."),
            ("monoT5", "https://arxiv.org/abs/2003.06713", "Sequence-to-sequence ranking by generating relevance labels."),
            ("Sentence Transformers reranker docs", "https://sbert.net/docs/cross_encoder/training_overview.html", "Practical cross-encoder training and evaluation patterns."),
        ],
    },
    {
        "slug": "local-inference",
        "title": "08 Local Inference",
        "directory": "08_local_inference",
        "script": "examples/08_local_inference/run.py",
        "command": "python 02_instruction_tuning/train.py --steps 120 && python 08_local_inference/run.py",
        "technique": "Local artifact loading and generation",
        "why": "A trained model becomes useful when it can be run from its released files. Local inference bridges training output and usable artifact: load a checkpoint, reconstruct the model, and generate without an API.",
        "look_at": ["checkpoint existence check", "rebuilding tokenizer and config", "load_state_dict", "generate from a local prompt"],
        "concepts": [
            ("Checkpoint", "A saved set of model weights plus enough metadata to rebuild the architecture and tokenizer."),
            ("Tokenizer state", "The vocabulary must match training. If token ids change, the learned weights no longer mean the same thing."),
            ("load_state_dict", "Restores learned parameters into a fresh model object so inference uses the trained artifact."),
            ("Local generation", "The final test is running from files on disk, without relying on an external model API."),
        ],
        "resources": [
            ("llama.cpp GGUF on Hugging Face", "https://huggingface.co/docs/hub/en/gguf-llamacpp", "Common local inference path for quantized GGUF models."),
            ("Ollama Modelfile", "https://docs.ollama.com/modelfile", "Simple local packaging surface for models, templates, parameters, and adapters."),
            ("MLX-LM", "https://github.com/ml-explore/mlx-lm", "Apple Silicon path for local generation and fine-tuning."),
            ("Hugging Face model cards", "https://huggingface.co/docs/hub/model-cards", "Artifact documentation that should ship with trained models."),
        ],
    },
]


PY_BUILTINS = set(dir(builtins))


def slugify(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)

    def link(match: re.Match[str]) -> str:
        label = match.group(1)
        href = html.escape(match.group(2), quote=True)
        return f'<a href="{href}">{label}</a>'

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = re.sub(
        r'(?<!href=")(https?://[^\s<]+)',
        r'<a href="\1">\1</a>',
        text,
    )
    return text


def highlight_python(code: str) -> str:
    """Small stdlib-only Python highlighter for teaching pages."""
    result: list[str] = []
    current_line = 1
    current_col = 0
    lines = code.splitlines(keepends=True)

    def append_gap(start_line: int, start_col: int) -> None:
        nonlocal current_line, current_col
        if current_line > len(lines):
            return
        while current_line < start_line and current_line <= len(lines):
            result.append(html.escape(lines[current_line - 1][current_col:]))
            current_line += 1
            current_col = 0
        if current_line <= len(lines) and current_col < start_col:
            result.append(html.escape(lines[current_line - 1][current_col:start_col]))
            current_col = start_col

    def token_class(tok_type: int, tok_text: str) -> str | None:
        if tok_type == tokenize.COMMENT:
            return "tok-comment"
        if tok_type == tokenize.STRING:
            return "tok-string"
        if tok_type == tokenize.NUMBER:
            return "tok-number"
        if tok_type == tokenize.NAME:
            if keyword.iskeyword(tok_text):
                return "tok-keyword"
            if tok_text in PY_BUILTINS:
                return "tok-builtin"
        return None

    try:
        tokens = tokenize.generate_tokens(io.StringIO(code).readline)
        for tok in tokens:
            if tok.type in {tokenize.ENCODING, tokenize.ENDMARKER}:
                continue
            start_line, start_col = tok.start
            end_line, end_col = tok.end
            append_gap(start_line, start_col)
            escaped = html.escape(tok.string)
            cls = token_class(tok.type, tok.string)
            result.append(f'<span class="{cls}">{escaped}</span>' if cls else escaped)
            current_line = end_line
            current_col = end_col
        append_gap(len(lines), len(lines[-1]) if lines else 0)
        return "".join(result)
    except tokenize.TokenError:
        return html.escape(code)


def code_block(code: str, language: str = "python") -> str:
    highlighted = highlight_python(code) if language == "python" else html.escape(code)
    rows = highlighted.splitlines()
    line_count_width = len(str(max(1, len(rows))))
    rendered_rows = []
    for i, row in enumerate(rows, start=1):
        source = row if row else "&nbsp;"
        rendered_rows.append(
            '<span class="code-line">'
            f'<span class="line-no">{str(i).rjust(line_count_width)}</span>'
            f'<span class="line-src">{source}</span>'
            "</span>"
        )
    return f'<pre class="code-frame" data-lang="{language}"><code>{"".join(rendered_rows)}</code></pre>'


def render_examples_page() -> tuple[str, str]:
    sections = []
    nav = []
    for area in EXAMPLE_AREAS:
        script = ROOT / area["script"]
        source = script.read_text(encoding="utf-8")
        nav.append(f'<a href="#{area["slug"]}">{html.escape(area["title"])}</a>')
        look_items = "".join(f"<li>{html.escape(item)}</li>" for item in area["look_at"])
        concepts = "".join(
            f"<dt><code>{html.escape(term)}</code></dt><dd>{html.escape(explanation)}</dd>"
            for term, explanation in area["concepts"]
        )
        resources = "".join(
            '<li>'
            f'<a href="{html.escape(url, quote=True)}">{html.escape(label)}</a>'
            f'<span>{html.escape(note)}</span>'
            "</li>"
            for label, url, note in area["resources"]
        )
        repo_url = (
            "https://github.com/BirgerMoell/useful-local-models-2026/tree/main/"
            f"{area['script'].rsplit('/', 1)[0]}"
        )
        sections.append(
            f"""
      <section class="example-section" id="{area["slug"]}">
        <div class="example-info">
          <p class="example-kicker">{html.escape(area["technique"])}</p>
          <h2>{html.escape(area["title"])}</h2>
          <h3 class="why-label">Why This Matters</h3>
          <p class="why-text">{html.escape(area["why"])}</p>
          <div class="concept-block">
            <h3>Key Concepts</h3>
            <dl>{concepts}</dl>
          </div>
          <div class="run-row">
            <code>{html.escape(area["command"])}</code>
            <button type="button" data-copy="{html.escape(area["command"], quote=True)}">Copy</button>
          </div>
          <div class="example-notes">
            <div>
              <h3>What To Notice</h3>
              <ul>{look_items}</ul>
            </div>
            <div>
              <h3>Papers And Resources</h3>
              <ul class="paper-list">{resources}</ul>
            </div>
          </div>
        </div>
        <div class="code-panel">
          <div class="code-head">
            <span>{html.escape(area["script"])}</span>
            <a href="{repo_url}">Source folder</a>
          </div>
          {code_block(source)}
        </div>
      </section>
"""
        )

    body = f"""
      <article class="examples-page">
        <section class="examples-hero">
          <p class="example-kicker">Training Examples</p>
          <h1>Tiny Training Examples</h1>
          <p>
            A readable map from technique to code. Each section shows why the area
            matters, which code paths carry the idea, and which papers or docs
            connect the minimal implementation to real systems.
          </p>
          <div class="example-nav" aria-label="Training example sections">
            {"".join(nav)}
          </div>
        </section>

        <section class="setup-strip" aria-labelledby="setup-title">
          <div>
            <h2 id="setup-title">Run Locally</h2>
            <p>From the repository root, create an environment and install PyTorch. The examples use synthetic data and write small artifacts under <code>examples/outputs/</code>.</p>
          </div>
          <div class="setup-commands">
            <code>cd examples</code>
            <code>python -m venv .venv</code>
            <code>source .venv/bin/activate</code>
            <code>pip install torch</code>
          </div>
        </section>
        {"".join(sections)}
      </article>
"""
    return "Tiny Training Examples", body


def render_markdown(markdown: str) -> tuple[str, str]:
    lines = markdown.splitlines()
    out: list[str] = []
    title = "Course Resource"
    in_code = False
    in_list = False
    in_table = False
    table_rows: list[list[str]] = []
    paragraph_lines: list[str] = []
    list_items: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if paragraph_lines:
            out.append(f"<p>{inline(' '.join(paragraph_lines))}</p>")
            paragraph_lines = []

    def close_list() -> None:
        nonlocal in_list, list_items
        if in_list:
            out.append("<ul>")
            for item in list_items:
                out.append(f"<li>{inline(item)}</li>")
            out.append("</ul>")
            in_list = False
            list_items = []

    def flush_table() -> None:
        nonlocal in_table, table_rows
        if not in_table:
            return
        out.append("<table>")
        for i, row in enumerate(table_rows):
            if i == 1 and all(re.fullmatch(r"\s*:?-{3,}:?\s*", cell) for cell in row):
                continue
            tag = "th" if i == 0 else "td"
            cells = "".join(f"<{tag}>{inline(cell.strip())}</{tag}>" for cell in row)
            out.append(f"<tr>{cells}</tr>")
        out.append("</table>")
        in_table = False
        table_rows = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            flush_table()
            close_list()
            if in_code:
                out.append("</code></pre>")
                in_code = False
            else:
                out.append("<pre><code>")
                in_code = True
            continue

        if in_code:
            out.append(html.escape(line))
            continue

        if not stripped:
            flush_paragraph()
            flush_table()
            close_list()
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph()
            close_list()
            in_table = True
            table_rows.append([cell for cell in stripped.strip("|").split("|")])
            continue
        flush_table()

        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            close_list()
            level = len(heading.group(1))
            text = heading.group(2)
            if level == 1:
                title = re.sub(r"`", "", text)
            out.append(f'<h{level} id="{slugify(text)}">{inline(text)}</h{level}>')
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            if not in_list:
                in_list = True
            list_items.append(stripped[2:])
            continue

        if in_list and line.startswith(("  ", "\t")) and list_items:
            list_items[-1] = f"{list_items[-1]} {stripped}"
            continue

        close_list()
        paragraph_lines.append(stripped)

    flush_paragraph()
    flush_table()
    close_list()
    if in_code:
        out.append("</code></pre>")
    return title, "\n".join(out)


def page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{html.escape(title)} - Useful Local Models</title>
    <link rel="icon" href="../favicon.svg" type="image/svg+xml">
    <link rel="stylesheet" href="resource.css">
  </head>
  <body>
    <header>
      <a href="../index.html">Useful Local Models</a>
    </header>
    <main>
      {body}
    </main>
    <script src="resource.js"></script>
  </body>
</html>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, source in DOCS.items():
        if name == "examples":
            title, body = render_examples_page()
        else:
            title, body = render_markdown(source.read_text(encoding="utf-8"))
        (OUT / f"{name}.html").write_text(page(title, body), encoding="utf-8")
    print(f"Wrote {len(DOCS)} resource pages to {OUT}")


if __name__ == "__main__":
    main()
