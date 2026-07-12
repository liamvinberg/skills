---
name: codex-delegate
description: Delegate work to Codex CLI workers (codex exec) on the current GPT model lineup. Use when the user says "codex" or wants work handed to a codex/GPT agent, wants a second implementation or opinion from a non-Claude model, or when another skill needs an implementation worker outside the session.
argument-hint: "task to delegate (or a spec path)"
---

# Delegate to Codex workers

A **worker** is one `codex exec` run: fresh context that re-grounds in the
files (codex auto-reads AGENTS.md), works inside codex's own sandbox, exits
with a final message. One worker per task — a task too big for one worker
wants splitting, not batching.

Workspace per task: the project's throwaway location if its conventions name
one (e.g. a gitignored `.scratch/<scope>/`), else `/tmp/codex-delegate/<task>/`.
Brief, log, and final message live there.

## 1. Lineup — read, never recall

The lineup changes too often to know from memory; codex refreshes its own
cache. Read it when you delegate:

```sh
jq -r '.models[] | select(.visibility=="list") | [.priority, .slug,
  (.supported_reasoning_levels|map(.effort)|join("/")), .description] | @tsv' \
  ~/.codex/models_cache.json | sort -n
```

**Model** — lowest `priority` is the flagship (2026-07: `gpt-5.6-sol`);
default to it. Step down the list only deliberately, for mechanical bulk work
where speed beats depth.

**Effort** — the flagship is strong at low effort: start low, turn it up.

- `medium` — default: bounded, spec-shaped tasks.
- `high` — substantial multi-file implementation.
- `xhigh` — cross-cutting architecture, concurrency, subtle state,
  security-sensitive behavior, hard debugging.
- `max` — hardest single problems, rare.
- `ultra` — the worker delegates sub-tasks itself; the most tokens by far.
  Only on the user's explicit ask.

Done when model and effort come from today's cache, not memory.

## 2. Brief

The brief becomes the worker's whole prompt. Write it to
`<dir>/<task>.brief.md`: goal, contracts (types/signatures), files to touch,
behavior detail, explicit out-of-scope list, gate commands (typecheck/tests),
and the report shape (what changed, gate output, open questions). End with
"Do not commit."

- A spec that already exists is referenced by path, not restated — brief =
  pointer + deltas. Same for PRDs, ADRs, issues.
- Taste lives in AGENTS.md, not the brief: codex auto-discovers it.
- Redact secrets — keys, tokens, PII have no place in a prompt.

Done when a worker could start from the brief alone. Delegation the user
didn't ask for: show task + model/effort and get a go first — an explicit
"hand this to codex" is already a go.

## 3. Spawn

```sh
codex exec -m <model> -c model_reasoning_effort=<effort> \
  -s workspace-write -c approval_policy=never \
  -o <dir>/<task>.final.md - < <dir>/<task>.brief.md 2>&1 | tee <dir>/<task>.log
```

Run as a background task — the stream is display-only for the user to watch;
you never read it. The worker's exit hands you back control; its final
message is the `-o` file. Stamp `git rev-parse HEAD` into the workspace as
the base ref before spawning.

Right after each spawn, capture the **resume handle** — the UUID ending the
newest rollout filename — and stamp it next to the base ref:

```sh
ls -t ~/.codex/sessions/*/*/*/*.jsonl | head -1
```

Read-only tasks (analysis, research, a second opinion) get `-s read-only`
instead. Parallel workers only when file-disjoint, each with its own
workspace, handle captured before the next spawn; overlapping work gets a
git worktree per worker via `-C`. Review delegation is its own subcommand:
`codex review --base <branch>` / `--uncommitted` (custom instructions as the
prompt).

## 4. Judge — claims are not evidence

The final message is a claim. Check it against artifacts, cheapest first:

1. **Gates** — rerun the gate commands yourself; never accept quoted output.
2. **Scope** — `git diff <base> --stat`: changed paths ⊆ the brief's file list.
3. **Tampering** — read test diffs in full: deleted assertions, skips,
   loosened expectations turn a green gate into a fail.
4. **Criteria** — walk the brief's behaviors one by one.
5. **Craft** — read the diff as your own PR: naming, altitude, the idiom of
   the surrounding code.

Verdict, sized by what's wrong: nothing → accept and commit yourself; small
residue → fix it yourself and rerun the gates; real rework → fix list
(`file:line`, one line per item) → fix round.

## 5. Fix rounds

The session carries the worker's context:

```sh
codex exec resume <uuid> -m <model> -c model_reasoning_effort=<effort> \
  -o <dir>/<task>.final.md "<fix list>"
```

Repeat model and effort — resume falls back to config defaults, not the
spawn's. Raise effort a rung when the worker keeps missing the same thing.
Max 2 rounds, then take over yourself and say so.

## 6. Report

Per task: verdict + one line of what shipped, and the resume handle for
later rounds.

## Knobs

| Knob | When |
|---|---|
| `-c service_tier=priority` | 1.5× speed at increased usage — deadline work |
| `-c mcp_servers={}` | Lean worker: skip MCP server startup |
| `-c sandbox_workspace_write.network_access=true` | Task needs installs/network inside the sandbox |
| `-i <image>` | Screenshot or design alongside the brief |
| `--output-schema <file>` | Machine-checkable final message (JSON Schema) |

`--ephemeral` forfeits resume — never on delegated work.
