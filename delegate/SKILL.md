---
name: delegate
description: Delegate implementation to CLI workers in disposable worktree lanes — plan, brief, judge, land; per-harness adapters (codex today) carry the worker mechanics.
argument-hint: "task to delegate (or a spec path) [harness]"
disable-model-invocation: true
---

# Delegate to workers

You are the brains: plan, write the brief, judge the result, land it. You do
not write implementation code — workers implement. One carve-out: edits under
~15 lines, do directly; delegation overhead exceeds the work. Your own
subagents (search, verify, review) never inherit your model — set a cheap one
explicitly.

A **worker** is one headless harness run: fresh context that re-grounds in
the files, works confined to its lane, exits with a final message. One worker
per task — a task too big for one worker wants splitting, not batching.

Workspace per task: the project's throwaway location if its conventions name
one (e.g. a gitignored `.scratch/<scope>/`), else `/tmp/delegate/<task>/`.
Brief, log, and final message live there; code changes live in the task's
lane (§3), never in your working tree.

## 1. Harness

The ask names the harness; unnamed → codex. Read that adapter before
spawning — it answers six things this file deliberately doesn't: model +
effort selection, the spawn command, the resume command, how writes stay
confined to the lane, where the final message lands, and the knobs.

- [codex.md](codex.md) — Codex CLI (`codex exec`), the default
- [pi.md](pi.md) — pi (`pi -p`)
- [omp.md](omp.md) — Oh My Pi (`omp -p`), pi with profiles + role models
- [opencode.md](opencode.md) — opencode (`opencode run`)

Codex confines writes at the kernel; the rest confine by the lane's cwd and
lean on the §5 scope-gate — which sees strays inside the lane but not an
absolute-path write to the main tree. For hard isolation of untrusted work,
pick codex; to point well-behaved workers at disjoint files (the parallel-lane
goal), cwd is enough. A new harness is a new sibling answering the same six.

**Effort** scales to the task; each adapter maps these rungs to its own knob:

- `medium` — default: bounded, spec-shaped tasks.
- `high` — substantial multi-file implementation.
- `xhigh` — cross-cutting architecture, concurrency, subtle state,
  security-sensitive behavior, hard debugging.
- `max` — hardest single problems, rare.

Done when model and effort come from the adapter's live source, not memory.

## 2. Brief

The brief becomes the worker's whole prompt. Write it to
`<dir>/<task>.brief.md`: goal, contracts (types/signatures), files to touch,
behavior detail, explicit out-of-scope list, gate commands (typecheck/tests),
and the report shape (what changed, gate output, open questions). End with
"Do not commit."

- A spec that already exists is referenced by path, not restated — brief =
  pointer + deltas. Same for PRDs, ADRs, issues. A brief outgrowing ~60
  lines means the task is too big — split it.
- Taste lives in the repo's agent docs (AGENTS.md), not the brief: workers
  discover it themselves.
- Redact secrets — keys, tokens, PII have no place in a prompt.

Done when a worker could start from the brief alone. Delegation the user
didn't ask for: show task + model/effort and get a go first — an explicit
"hand this to a worker" is already a go.

## 3. Lane

Implementation never touches your working tree. Each task — or chain of
dependent tasks — gets a **lane**: a disposable worktree and branch cut from
the base commit, landed and erased the moment the work is in. Two or more
lanes at once → read [parallel.md](parallel.md) before spawning any.

Before cutting, check `git worktree list` for `lane/*` leftovers: provably
empty (clean tree, branch merged) → remove; holding work → surface it, never
sweep blind — it may be another session's live lane. Name taken → suffix
yours.

```sh
base=$(git rev-parse HEAD)          # stamp into the workspace
git worktree add ../<repo>.lanes/<name> -b lane/<name> "$base"
```

Then warm the deps the repo's native way (pnpm:
`pnpm install --prefer-offline` inside the worktree).

Done when the worktree sits at the stamped base with deps warm.

## 4. Spawn

Spawn with the adapter's command, always as a background task — the stream is
display-only for the user to watch; you never read it. The worker's exit
hands you back control; its final message is the file the adapter's command
writes.

Right after each spawn, capture the **resume handle** the adapter defines,
and stamp it next to the base ref.

Read-only tasks (analysis, research, a second opinion) run in the adapter's
read-only mode from the main tree — no lane. Parallel workers: one lane each
([parallel.md](parallel.md)), each with its own workspace, handle captured
before the next spawn.

## 5. Judge — claims are not evidence

The final message is a claim. Check it against artifacts, cheapest first:

1. **Gates** — rerun the gate commands yourself, inside the lane; never
   accept quoted output.
2. **Scope** — `git -C <wt> status --porcelain` (untracked included):
   changed paths ⊆ the brief's file list.
3. **Tampering** — read test diffs in full: deleted assertions, skips,
   loosened expectations turn a green gate into a fail.
4. **Criteria** — walk the brief's behaviors one by one.
5. **Craft** — read the diff as your own PR: naming, altitude, the idiom of
   the surrounding code.

Verdict, sized by what's wrong: nothing → accept and land (§7); small
residue → fix it yourself in the lane and rerun the gates; real rework →
fix list (`file:line`, one line per item) → fix round.

## 6. Fix rounds

The worker's session carries its context: resume it with the adapter's
resume command, the fix list as the prompt. Raise effort a rung when the
worker keeps missing the same thing. Max 2 rounds, then take over yourself
and say so.

## 7. Land

Accept → you commit, in the lane: one atomic commit per task, your message,
never the worker's. Chain finished → land it — rebase, fast-forward, erase,
one move; a landed lane leaves nothing behind:

```sh
git -C <wt> rebase <base-branch>
git merge --ff-only lane/<name>            # from the main tree
git worktree remove --force <wt> && git branch -d lane/<name>
```

Rebase conflict → the resolving-merge-conflicts skill, then finish landing.
Main tree dirty at land time → surface it and wait; landing never mixes with
uncommitted work that isn't yours.

Done when the base branch carries the commits and `git worktree list` shows
no lane for this task.

## 8. Report

Per task: verdict + one line of what shipped, and the resume handle for
later rounds.
