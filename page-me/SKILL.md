---
name: page-me
description: Communicate through a round-trip HTML page served locally, when chat text would flatten the content. Show the user something interactive (comparison, visualization, parameter playground, walkthrough) or collect structured answers (forms, sign-offs, sequential interviews) whose submits flow back into the session. Use when the user asks for a page, form, slider, or interactive anything, when an explanation needs custom inputs or live visuals, or when another skill needs page delivery for its questions or output.
---

A **round-trip page** is a single-file HTML page served by a long-lived local listener, wired to the session in both directions: you rewrite its state and the page re-renders without a reload or a listener restart; the user submits and the answer lands back in the session. A page can **show** (explain, visualize, keep a live surface current), **ask** (collect structured answers), or do both; the wiring is identical either way.

## Steps

1. **Workspace.** Create a fresh directory per page: the project's own throwaway-prototype location if its conventions name one (e.g. a gitignored `scratchpad/`), else `/tmp/html-comm/<slug>/`. Done when the directory exists outside version control.

2. **Author.** Pick the recipe matching the page's shape in [PATTERNS.md](PATTERNS.md) before writing anything. Copy `assets/template.html` to `<dir>/index.html` and replace its REPLACE markers, keeping the helpers. Static content lives in the HTML; anything that updates lives in `<dir>/state.json` and renders through `watchState`. The template's baseline is the entire theme: add no hue, no fonts, no decoration, and keep wide content scrolling inside its own container. Done when index.html renders your content with the helpers intact.

3. **Listen.** Run `python3 <skill>/assets/serve.py <dir>` in the background and parse the printed `LISTENING http://127.0.0.1:<port>` line. One listener serves the page for its whole life, across any number of submits and state rewrites. Done when fetching the URL returns your page.

4. **Reach the user.** The page must be reachable by whoever it is for. Private reach is the default; expose the page publicly only when the user explicitly asks for an outside answerer. When the project or user configuration names a reach mechanism for remote sessions, prefer it.
   - Local session: `open <url>` (macOS) or `xdg-open <url>`.
   - Remote session: serve through the environment's private tunnel. With tailscale: `tailscale serve --bg <port>`, announce the https tailnet URL it prints, and escalate to `tailscale funnel` only on that explicit ask. The universal fallback is handing the user `ssh -L <port>:127.0.0.1:<port> <host>` plus the localhost URL.
   Done when the URL is announced in chat.

5. **The round trip.** A page that only shows has nothing to wait for: rewrite `state.json` whenever the session teaches the page something new, and move to teardown once the user closes it out in chat. A page that asks waits for submits without burning attention: watch the listener's output for `SUBMIT ` lines. If your harness has a background file-watch or monitor tool, point it at the listener's output with a filter on `^SUBMIT `. If it does not, `python3 serve.py --await <dir>` blocks until the next answer arrives, and running that in the background makes its exit the wake-up signal. On each answer: read the JSON, act on it, rewrite `state.json` in place. Never restart the listener to change the page. When an answer asks a factual question, research it and put the findings in the next state. Done when the page's purpose is met: every planned screen answered, or the user closes it out in chat.

6. **Teardown.** Kill the listener. If a tunnel was configured, remove it (tailscale: `tailscale serve --https=443 off`, or `funnel --https=443 off`). Graduate durable conclusions to wherever the invoking task records them (ticket, doc, chat summary); the page itself is throwaway. Done when nothing listens and no serve config remains.

## Answers

`POST /submit` accepts any JSON; the listener stamps `ts` and appends it to `<dir>/answers.jsonl`. Give every screen a `qid` field so multi-question pages stay attributable. Anyone holding the URL can answer: treat submissions as the user's delegates, and include a name field in the form when it matters who answered.

## Safety

The page is reachable by whoever has the URL. Never render secrets, tokens, or private data you would not paste in a group chat; a public tunnel is the public internet. Everything under `<dir>` is disposable once conclusions have graduated.
