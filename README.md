# Agent skills

Portable [Agent Skills](https://skills.sh) (standard `SKILL.md`), installable cross-agent (Claude Code, Cursor, Copilot, Codex, Cline, …) from this repo.

| Skill | For | Install |
|---|---|---|
| `beam` | Temporarily serve a local file or folder to your other devices over your Tailscale tailnet | `npx skills add liamvinberg/skills --skill beam` |
| `delegate` | Delegate implementation to CLI workers in disposable worktree lanes: a harness-agnostic core (brief, lane, artifact-based judging, fix rounds, land) plus per-harness adapters — codex today, with model/effort picked from codex's own live lineup cache; parallel fan-out with dependency chains, auto-landed onto your branch and erased | `npx skills add liamvinberg/skills --skill delegate` |
| `page-me` | The agent pages you: round-trip HTML pages for interactive showings (comparisons, playgrounds, visualizations) and structured answer collection (forms, interviews), with a local listener that feeds submits back into the session | `npx skills add liamvinberg/skills --skill page-me` |

Install everything: `npx skills add liamvinberg/skills`. Updates: `npx skills update`.

## Notes

- Pages are single-file HTML with no dependencies, on a monochrome reading baseline backed by legibility research (dark-on-light comprehension, halation-safe dark variant, system type, ~66ch measure).
- The listener is stdlib Python, long-lived, with an `--await` mode for agents without a file-watch tool.
- The listener-plus-watcher idea follows [f-labs-io/agent-html-skills](https://github.com/f-labs-io/agent-html-skills) (MIT).
