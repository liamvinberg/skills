# pi adapter

pi workers via `pi -p`. pi reads AGENTS.md/CLAUDE.md by default (disable with
`--no-context-files`) and carries read/bash/edit/write tools. No kernel
sandbox: a lane pins writes by running pi with the lane as its cwd, and the
§5 scope-gate catches strays inside it. `-a` trusts the lane's project-local
config so the run doesn't stall on a trust prompt.

## Model + effort

List live — there's no fixed flagship; the strongest model depends on your
configured providers:

```sh
pi --list-models [search]
```

`--model <provider/id>` selects (a bare id uses `--provider`, default
google). Effort is `--thinking off|minimal|low|medium|high|xhigh`; only
models whose list row shows `thinking yes` honor it. Map the core ladder
medium→medium, high→high, xhigh and max→xhigh (pi tops out at xhigh).

## Spawn

```sh
( cd <wt> && pi -p -a --model <model> --thinking <level> \
    "$(cat <dir>/<task>.brief.md)" > <dir>/<task>.final.md 2> <dir>/<task>.log )
```

Text-mode stdout is the final message. Pin a deterministic resume handle up
front with `--session-id <name>` — sessions are keyed by cwd, so the lane
already namespaces them.

Read-only (analysis, second opinion) from the main tree, no lane:
`pi -p -xt edit,write,bash "<question>"`.

## Resume

From the lane's cwd, `--continue` picks that lane's last worker — exactly the
one a fix round targets:

```sh
( cd <wt> && pi -p -a -c --model <model> --thinking <level> \
    "<fix list>" > <dir>/<task>.final.md 2> <dir>/<task>.log )
```

Or target an explicit session with `--session <id-prefix>`.

## Knobs

| Knob | When |
|---|---|
| `--session-id <name>` | Deterministic handle instead of capture |
| `--mode json` | Machine-readable events instead of text |
| `-xt bash` | Bar shell execution — edits only |
| `--no-extensions` | Lean worker: skip extension discovery |
| `@file` args | Attach files/images alongside the brief |
