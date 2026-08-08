---
name: exam-checkpoint
description: Mid-exam checkpoint for the EDA/ML admission task — reconcile code, README, and AI_USAGE.md, run lightweight verification, and report drift or unverified claims. Use when the user asks for a checkpoint, before declaring a unit of work complete, or near the end of the time box.
---

# Exam checkpoint

Reconcile the repository state with its documentation. **Never commit, push, or amend history.**
Never invent metrics, verifications, or decisions the user did not make.

## Steps

1. **Scope the work.** Run `git status` and `git diff` (plus `git diff --stat`) and list what changed since the last
   checkpoint — the previous `AI_USAGE.md` entry marks it. Include untracked notebooks and modules.
2. **AI_USAGE.md.** If AI materially contributed to that work, append one entry using the template in the file: AI help,
   what was verified (by the user or by running code), rejected or changed suggestions, decisions that are the user's.
   Skip trivial edits. If you do not know whether the user verified something, ask or leave it explicitly unfilled.
3. **README.md.** If implemented behavior, metrics, or conclusions changed, update the affected sections so README
   describes only what exists and only numbers actually produced. Remove claims that no longer hold.
4. **Verify.** Run whatever is cheap and currently applicable, e.g.:
    - `uv run ruff check .`
    - `uv run pytest -q` (only if tests exist)
    - re-execute the cell/script behind any number quoted in README, or confirm it came from a real run in this session
5. **Report** concisely:
    - discrepancies between code and documentation
    - numbers or claims in README/notebooks that were not actually produced
    - unfinished or stubbed work, and requirements from the task statement not yet addressed
    - failed checks, with the real output
    - suggested next action given the remaining time

Report honestly: if a check could not be run, say so instead of implying it passed.
