# Codex adapter

Codex CLI workers via `codex exec`. Codex auto-reads AGENTS.md and brings
its own sandbox: `-C <wt>` roots it in the lane and `-s workspace-write`
confines writes there — lane confinement comes free.

## Lineup — read, never recall

The lineup changes too often to know from memory; codex refreshes its own
cache. Read it when you delegate:

```sh
jq -r '.models[] | select(.visibility=="list") | [.priority, .slug,
  (.supported_reasoning_levels|map(.effort)|join("/")), .description] | @tsv' \
  ~/.codex/models_cache.json | sort -n
```

**Model** — lowest `priority` is the flagship; default to it. Step down the
list only deliberately, for mechanical bulk work where speed beats depth.

**Effort** — flag is `-c model_reasoning_effort=<level>`, levels
`low|medium|high|xhigh|max`. The flagship is strong low, so start low and
turn it up the core ladder. Two codex-only rungs frame it: `low` below the
ladder's medium for trivial work, and `ultra` above `max` — the worker
delegates sub-tasks itself, the most tokens by far, only on the user's
explicit ask.

## Spawn

```sh
codex exec -C <wt> -m <model> -c model_reasoning_effort=<effort> \
  -s workspace-write -c approval_policy=never \
  -o <dir>/<task>.final.md - < <dir>/<task>.brief.md 2>&1 | tee <dir>/<task>.log
```

The final message is the `-o` file. The resume handle is the UUID ending the
newest rollout filename:

```sh
ls -t ~/.codex/sessions/*/*/*/*.jsonl | head -1
```

Read-only mode: `-s read-only` replacing `-s workspace-write`. Review
delegation is its own subcommand: `codex review --base <branch>` /
`--uncommitted` (custom instructions as the prompt).

## Resume

```sh
codex exec resume <uuid> -C <wt> -m <model> -c model_reasoning_effort=<effort> \
  -o <dir>/<task>.final.md "<fix list>"
```

Repeat model, effort, and `-C` — resume falls back to config defaults, not
the spawn's.

## Knobs

| Knob | When |
|---|---|
| `-c service_tier=priority` | 1.5× speed at increased usage — deadline work |
| `-c mcp_servers={}` | Lean worker: skip MCP server startup |
| `-c sandbox_workspace_write.network_access=true` | Task needs installs/network inside the sandbox |
| `-i <image>` | Screenshot or design alongside the brief |
| `--output-schema <file>` | Machine-checkable final message (JSON Schema) |

`--ephemeral` forfeits resume — never on delegated work.
