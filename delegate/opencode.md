# opencode adapter

opencode workers via `opencode run`. Reads AGENTS.md by default. No kernel
sandbox: `--dir <wt>` runs the worker in the lane and
`--dangerously-skip-permissions` keeps it unattended; the §5 scope-gate
catches strays inside the lane.

## Model + effort

```sh
opencode models [provider]
```

`-m provider/model` selects — the free `opencode-go/*` lineup carries GLM,
Kimi, MiniMax and more, all free. Effort is provider-specific via
`--variant`, which exposes fewer rungs than the ladder: medium→no flag,
high and xhigh→`--variant high`, max→`--variant max`. Models without variants
ignore it. `--variant minimal` sits below the ladder for trivial work.

## Spawn

```sh
opencode run --dir <wt> --dangerously-skip-permissions \
  -m <model> [--variant <effort>] "$(cat <dir>/<task>.brief.md)" \
  > <dir>/<task>.final.md 2> <dir>/<task>.log
```

Stdout is the final message (`--format json` for raw events). Capture the
resume handle from `opencode session list` (newest first) right after
spawning.

Read-only from the main tree, no lane: `--agent plan` (opencode's built-in
read-only agent) in place of the skip-permissions flag.

## Resume

```sh
opencode run --dir <wt> --dangerously-skip-permissions -s <session-id> \
  -m <model> "<fix list>" > <dir>/<task>.final.md 2> <dir>/<task>.log
```

`-c` continues the lane's last session if you didn't capture the id.

## Knobs

| Knob | When |
|---|---|
| `--agent <name>` | Run under a configured agent (`plan` = read-only) |
| `--variant <effort>` | Provider reasoning effort: minimal/high/max |
| `--format json` | Machine-readable events instead of formatted text |
| `--fork` | Branch a session instead of continuing it in place |
| `-f <file>` | Attach files/images alongside the brief |
