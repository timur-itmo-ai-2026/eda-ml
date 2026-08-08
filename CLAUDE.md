# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

EDA and a baseline ML model, written as an entrance-exam assignment for the ITMO
"Artificial Intelligence" master's program (README is in Russian). The repo is currently
scaffolding only — `src/eda_ml/__init__.py` is empty, there are no tests, and `AI_USAGE.md`
exists but is empty (it is presumably meant to document AI assistance for the submission).

## Toolchain

uv-managed, Python 3.13 (`.python-version`), src layout with the `uv_build` backend, so
`eda_ml` is importable only via the project's own environment install. `uv.lock` is committed —
keep it in sync and never hand-edit it.

```powershell
uv sync                      # create/update .venv from uv.lock (includes the dev group)
uv run python -c "import eda_ml"
uv run ruff check .          # lint (ruff is a dev dep; there is no [tool.ruff] config yet — defaults apply)
uv run ruff format .
uv run pytest                # no tests exist yet
uv run pytest tests/test_x.py::test_name   # single test
uv run jupyter lab           # notebooks; ipykernel is installed for the project env
```

Prefer `uv run <cmd>` over activating `.venv` manually, and `uv add <pkg>` / `uv add --dev <pkg>`
over editing `pyproject.toml` dependency lists by hand.

## Conventions to preserve as code lands

- Library code belongs under `src/eda_ml/`; notebooks should import from it rather than
  redefining logic inline, so the analysis stays reproducible and testable.
- Data files are not in the repo and `.gitignore` does not exempt any data directory — do not
  commit datasets or generated artifacts (figures, model pickles) without an explicit
  `.gitignore` decision first.
- pandas 3.x and numpy 2.x are pinned as lower bounds; `pyarrow` is a direct dependency, so
  prefer Arrow-backed dtypes and Parquet over CSV where a choice exists.
