# CLAUDE.md

Instructions for Claude Code in this repository.

## Project context

- Repository for the ITMO "Artificial Intelligence" master's admission task **"EDA and Machine Learning"** (Task 1 of
  the selection stage). Time limit: **2 hours**.
- Python 3.13, `uv` as package/environment manager, src layout with the `eda_ml` package.
- Reusable logic goes into `src/eda_ml/` when it is actually reused or worth testing. Exploratory work may live in
  notebooks.
- Documentation for the committee (`README.md`, `AI_USAGE.md`) is in Russian.
- **Do not overengineer a 2-hour solution.** No abstraction layers, config frameworks, CLIs, or CI pipelines unless the
  task explicitly asks for them.

```powershell
uv sync                      # environment from uv.lock (includes dev group)
uv run ruff check . ; uv run ruff format .
uv run pytest                # only if tests exist
uv run jupyter lab
```

Prefer `uv run <cmd>` over activating `.venv`; prefer `uv add <pkg>` / `uv add --dev <pkg>`
over hand-editing `pyproject.toml`. Never hand-edit `uv.lock`.

## Exam workflow

**Read the COMPLETE task before implementing anything.** First extract and restate:
explicit requirements, requested outputs and their exact formats, constraints, evaluation criteria, submission
requirements. Answer-format and filtering conditions ("only non-empty",
"in range from … to …") must be reproduced literally — most lost points come from inattentive filtering, not from bad
code.

- **Never assume the ML problem type** (regression / classification / clustering / anomaly detection / other) or the
  data modality before inspecting the actual task and data.
- Inspect data quality before modeling: shape, schema and dtypes, missing values, duplicates (including the same entity
  repeated under partially filled identifiers), suspicious/garbage values, contradictions between fields, distributions,
  and target quality where applicable.
- Support every important analytical conclusion with an actual computed value, table, or plot.
- Start with a **simple defensible baseline**. Improve only after it works end to end.
- Choose validation strategy and metrics from the actual problem, and justify the choice (e.g. why accuracy is
  misleading under class imbalance; grouped/temporal splits when rows are not independent).
- Explicitly check for **target leakage** and **preprocessing leakage** (fit transforms inside the training fold only).
- Prefer correctness, reproducibility, and explainability over sophistication. Fix random seeds. State assumptions
  instead of hiding them.
- **Run the code and verify outputs. Never report a number that was not actually produced.**
  Sanity-check shapes and magnitudes; a plausible-looking wrong answer is the main failure mode.
- Do not optimize a metric blindly — know what changed and why it helped.
- Reserve the last 10–15 minutes for a final pass: re-read the task, check answer formats, verify README against the
  code.
- Do not add dependencies unless useful for the actual task.
- Do not make destructive or irreversible changes without a clear reason. Do not commit or push unless asked.
- Datasets and generated artifacts (figures, model files) are not committed unless a
  `.gitignore` decision is made first.

## Documentation workflow

`README.md` is the human-facing description of the submitted solution, in Russian.

- Keep it synchronized with the **actually implemented** solution and **actually measured**
  results.
- Never put invented metrics, conclusions, or completed-work claims in README. If something is not done, either omit the
  section or mark it honestly as not done.

## AI usage protocol

`AI_USAGE.md` is the audit trail of AI assistance, required by the admission rules and used at the interview to verify
authorship.

After every meaningful completed unit of work in which AI materially contributed, **and always before telling the user
that a requested unit of work is complete**:

1. update `AI_USAGE.md`;
2. briefly record what AI helped with;
3. record what the user or the code/data execution verified;
4. record important AI suggestions that were rejected or changed, when applicable;
5. record important decisions that remain the user's.

Never fabricate verification or human decisions — if something was not verified, say so, or leave it for the user to
fill in.

Do **not** log trivial operations: reading a file, formatting, renames, obvious mechanical edits.
