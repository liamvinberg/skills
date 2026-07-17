# omp adapter (Oh My Pi)

omp workers via `omp -p` — pi's engine with profiles, role models, and an
approval mode. Reads AGENTS.md/CLAUDE.md by default (`--no-rules` disables).
No kernel sandbox: `--cwd <wt>` runs the worker in the lane and
`--auto-approve` keeps it unattended; the §5 scope-gate catches strays inside
the lane.

## Model + effort

```sh
omp models [ls|find|<provider>] [pattern] [--json]
```

`--model <fuzzy>` selects with no fixed flagship — fuzzy-match what you want
("opus", "glm", "provider/id"). Effort is
`--thinking off|minimal|low|medium|high|xhigh|auto`; the model's list row
shows which levels it honors. Map the core ladder medium→medium, high→high,
xhigh and max→xhigh (xhigh the cap). Role models split brains in one run:
`--slow` for the hard turns, `--smol` for cheap ones.

## Spawn

```sh
omp -p --cwd <wt> --auto-approve --model <model> --thinking <level> \
  "$(cat <dir>/<task>.brief.md)" > <dir>/<task>.final.md 2> <dir>/<task>.log
```

Text-mode stdout is the final message. `--approval-mode write` in place of
`--auto-approve` bars shell escapes while allowing edits — tighter
confinement when the task is edits-only.

Read-only from the main tree, no lane: drop `--cwd` and allowlist the read
tool — omp has no exclude form — with `--tools read`.

## Resume

Per-cwd sessions mean `--continue` from the lane resumes its last worker:

```sh
omp -p --cwd <wt> --auto-approve -c --model <model> --thinking <level> \
  "<fix list>" > <dir>/<task>.final.md 2> <dir>/<task>.log
```

Or `-r <id-prefix>` to target an explicit session.

## Knobs

| Knob | When |
|---|---|
| `--profile <name>` | Isolated auth/sessions/caches — separate worker identity |
| `--approval-mode write` | Auto-approve edits but bar bash |
| `--slow` / `--smol` / `--plan` | Per-role model overrides in one run |
| `--max-time <sec>` | Hard wall-clock cap on the worker |
| `--mode json` | Machine-readable events instead of text |
