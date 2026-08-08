# CLAUDE.md

Instructions for Claude Code in this repository.

## Project context

- Repository for the ITMO "Artificial Intelligence" master's admission task **"EDA and Machine Learning"**.
  Total time limit: **2 hours**.
- Python 3.13, `uv` as package/environment manager, src layout with the `eda_ml` package.
- `TASK.md` holds the task legend and the submission rules. It is context only — **never modify it**.
- Documentation for the committee (`README.md`, `AI_USAGE.md`) is in Russian.

```powershell
uv sync                      # environment from uv.lock (includes dev group)
uv run ruff check . ; uv run ruff format .
uv run pytest                # only if tests exist
uv run jupyter lab
```

Prefer `uv run <cmd>` over activating `.venv`; prefer `uv add <pkg>` / `uv add --dev <pkg>`
over hand-editing `pyproject.toml`. Never hand-edit `uv.lock`.

## Task at hand

Binary classification: predict `relief_granted` (1 = the company closed the complaint with monetary or non-monetary
relief) for consumer complaints, to prioritize escalation. Features: product, sub-product, issue type, company, state,
ZIP, submission channel, date received, date sent to company, plus the raw narrative text
`Consumer.Complaint.Narrative`.

Data are deliberately dirty: missing values, duplicates, inconsistent category spellings, **several date formats**,
garbage values, and templated mass submissions of identical text. `complaints_test.csv` covers the **last months of
observations — the future relative to train**.

Datasets live in `data/` (git-ignored): `complaints_train.csv` (~7.7 GB), `complaints_test.csv`,
`sample_submission.csv`. **Never modify or overwrite the original datasets.** Never commit datasets, caches, or other
large generated artifacts.

## Interaction model

The user does **not** delegate the whole exam. Exam questions arrive **one at a time**, e.g. a message containing `A1`
followed by the exact wording, then `A2`, `B1`, `C2`, and so on.

- The question in the user's current message is the **authoritative task for the current work unit**.
- Solve **only that question**. Do not invent missing questions and do not answer questions the user has not sent.
- Read the wording literally and identify: what exactly must be calculated or explained; filtering conditions; required
  units, rounding and output format; which dataset(s) to use. Answer-format and filtering conditions ("only non-empty",
  "in range from … to …") must be reproduced literally — most lost points come from inattentive filtering, not bad code.
- If the wording is genuinely ambiguous **and** the ambiguity can change the answer, say so briefly before choosing an
  interpretation. Otherwise proceed immediately without unnecessary discussion.

## Notebook is the primary deliverable

The submitted artifact is `notebooks/solution.ipynb`. Create it when the first real question arrives.

For **every** question, append in this order:

1. a Markdown cell with the identifier, a short title, and the **original question verbatim**;
2. the reproducible code that answers it;
3. the preserved executed output, table or visualization;
4. a concise **Russian** answer/conclusion.

```markdown
## A1 — <short descriptive title>

**Задание**

<exact original wording supplied by the user>

[code cell(s)]

[output / visualization]

**Ответ:** ...

**Вывод:** ...   # only when a conclusion is actually useful
```

Keep identifiers easy to locate for a human reviewer and for automated evaluation. Never put Claude prompts,
conversation transcript or internal planning into the notebook — only the exam question, reproducible solution, evidence
and answer.

Do not rewrite previously completed answers unless new evidence shows they are wrong. If that happens, tell the user
explicitly what changed and why.

## Data workflow

**DuckDB is the default tool** for working with the full CSVs: schema inspection, row counts, filtering, grouping and
aggregation, missing-value and duplicate analysis, date-range checks, and extracting manageable subsets or feature
tables.

- **Do not eagerly load the training CSV into pandas.** Use pandas / NumPy / scikit-learn once the data are reduced to a
  safe in-memory size, or where they are the right tool for modeling and visualization.
- Do not introduce Polars or another large-data framework unless a specific question gives a concrete reason.
- Do not convert the whole dataset to Parquet merely because it is possible. If repeated CSV scans become a real
  bottleneck, weigh cost against benefit first.
- Do not trust inferred DuckDB CSV types blindly — the data contain dirty values and multiple date formats. If inference
  looks suspicious or fails, read the affected fields as strings and parse them deliberately.
- **Never use error-skipping options just to make a query succeed** without understanding what would be discarded.

## Analytical correctness

All calculations must use only the provided exam files; the external CFPB database may differ.

For every numerical answer: derive it from executed code; verify the denominator and the filters; check missing-value
treatment; check date interpretation where relevant; keep enough code and output in the notebook to reproduce it.
**Never report a number that was not actually produced** — a plausible-looking wrong answer is the main failure mode.
Sanity-check shapes and magnitudes. Support every analytical conclusion with a computed value, table or plot.

Because test is the future relative to train, when analyzing or modeling: respect temporal ordering; check temporal
leakage, target leakage and preprocessing leakage (fit transforms inside the training fold only); consider
duplicate/templated-complaint leakage across validation boundaries; consider whether each feature would actually be
available at prediction time; inspect train/test drift where relevant.

Do not drop columns merely because they look suspicious — investigate and justify using the actual data and task. Fix
random seeds. State assumptions instead of hiding them.

## Modeling

Do not start modeling unless the current question requires it. When it does:

- start with a simple defensible baseline and get it working end to end;
- use a validation strategy appropriate to the temporal setup, and justify it;
- choose metrics from the actual question and the business objective (e.g. why accuracy misleads under class imbalance);
- explain important choices; do not optimize a metric blindly — know what changed and why it helped;
- prefer a correct, reproducible, explainable baseline over sophistication.

The narrative text may carry signal, but do not build an expensive NLP pipeline unless the question and the evidence
justify it.

## Timebox and priorities

Official guidance: A ≈ 15 min, B ≈ 45 min, the remaining time split between C and P. The user applies to the
**Artificial Intelligence** program, therefore:

- A and B are mandatory;
- after A and B, prioritize C;
- **do not work on P unless the user explicitly asks.**

Avoid overengineering. No abstraction layers, config frameworks, CLIs, or CI pipelines. Put code in `src/eda_ml/` only
when it materially helps solve the actual questions faster or more reliably; otherwise keep it in the notebook.
Do not add dependencies unless useful for the actual task. Do not make destructive or irreversible changes without a
clear reason. **Do not commit or push unless explicitly asked.**

## AI_USAGE.md

`AI_USAGE.md` is the audit trail of AI assistance required by the admission rules and used at the interview to verify
authorship.

After **every** completed exam question in which AI materially contributed, and **before** telling the user the question
is complete, append a concise entry identified by the question number, recording:

- what AI helped to implement or analyze;
- what was verified — clearly distinguishing **verification by executing code / inspecting data** from a **decision
  explicitly made by the user**;
- significant AI suggestions that were rejected or changed, when applicable.

Never fabricate a user decision or an independent verification. Do not log trivial operations: file reads, formatting,
`git status`, mechanical notebook edits. Do not copy prompts or conversation transcripts.

## README.md

`README.md` describes the project overall and how to reproduce it, in Russian. **Do not rewrite it after every
question.** Update it only when the setup, dependencies, run instructions, solution architecture or final high-level
results materially change — and only with results that were actually measured. The notebook remains the authoritative
evidence for individual answers. Do not modify README unless the user asks or one of those material changes occurred.

## Completion protocol for each question

Before telling the user a question is complete:

1. verify the exact question appears in `notebooks/solution.ipynb`;
2. verify its code is reproducible;
3. verify the displayed answer follows from the executed output;
4. verify no required filtering or format condition was missed;
5. update `AI_USAGE.md`;
6. do not commit or push.

Then report concisely: the answer; where it is in the notebook; what was verified; any remaining uncertainty.
**Then stop and wait for the next exam question.**

## Final exam checkpoint

Only when the user explicitly says the assignment is finishing: review all mandatory A and B questions and the requested
C questions; run the appropriate checks; ensure the notebook is reproducible; check README only for necessary final
synchronization; review `AI_USAGE.md`; inspect `git diff` and `git status`; flag anything incomplete or unverified.
Do not commit or push unless explicitly asked.
