# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project Architecture

See [`ARCH.md`](./ARCH.md) for the full, auto-maintained file-tree map and component overview — the primary entry point for orienting in this repo. The tree refreshes automatically on every commit via `.githooks/pre-commit`; refresh manually with `python3 .githooks/gen_arch.py`. After cloning, activate the hook once with `git config core.hooksPath .githooks`. Use the `code-explorer` agent for deeper tracing.

This is a single-file GIMP 3.0 Python-Fu script (`batch_collage_gimp_3.0.py`) run inside GIMP's Python Console; behavior is controlled by the constants at the top of that file.

## Agent skills

### Issue tracker

Issues tracked in this repo's GitHub Issues via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default five-role vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.

