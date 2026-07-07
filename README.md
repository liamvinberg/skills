# Agent skills

Portable [Agent Skills](https://skills.sh) (standard `SKILL.md`), installable cross-agent (Claude Code, Cursor, Copilot, Codex, Cline, …) from this repo.

| Skill | For | Install |
|---|---|---|
| `html-communication` | Communicating through round-trip HTML pages: interactive showings (comparisons, playgrounds, visualizations) and structured answer collection (forms, interviews) with a local listener that feeds submits back into the agent session | `npx skills add liamvinberg/skills --skill html-communication` |

Install everything: `npx skills add liamvinberg/skills`. Updates: `npx skills update`.

## Notes

- Pages are single-file HTML with no dependencies, on a monochrome reading baseline backed by legibility research (dark-on-light comprehension, halation-safe dark variant, system type, ~66ch measure).
- The listener is stdlib Python, long-lived, with an `--await` mode for agents without a file-watch tool.
- The listener-plus-watcher idea follows [f-labs-io/agent-html-skills](https://github.com/f-labs-io/agent-html-skills) (MIT).
