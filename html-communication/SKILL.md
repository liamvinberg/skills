---
name: html-communication
description: Communicate through a round-trip HTML page served locally, when chat text would flatten the content. Show the user something interactive (comparison, visualization, parameter playground, walkthrough) or collect structured answers (forms, sign-offs, sequential interviews) whose submits flow back into the session. Use when the user asks for a page, form, slider, or interactive anything, when an explanation needs custom inputs or live visuals, or when another skill needs page delivery for its questions or output.
---

A **round-trip page** is a single-file HTML page served by a long-lived local listener. The user reads and interacts, Submit posts back to the session, you act on the answer and rewrite the page's state, and the page re-renders without a reload or a listener restart.

## Steps

1. **Workspace.** Create a fresh directory per page: the project's own throwaway-prototype location if its conventions name one (e.g. a gitignored `scratchpad/`), else `/tmp/html-comm/<slug>/`. Done when the directory exists outside version control.

2. **Author.** Pick the recipe matching the page's shape in [PATTERNS.md](PATTERNS.md) before writing anything. Copy `assets/template.html` to `<dir>/index.html` and replace its REPLACE markers, keeping the helpers. Static content lives in the HTML; anything that updates lives in `<dir>/state.json` and renders through `watchState`. The template's baseline is the entire theme: add no hue, no fonts, no decoration, and keep wide content scrolling inside its own container. Done when index.html renders your content with the helpers intact.

3. **Listen.** Run `python3 <skill>/assets/serve.py <dir>` in the background and parse the printed `LISTENING http://127.0.0.1:<port>` line. One listener serves the page for its whole life, across any number of submits and state rewrites. Done when fetching the URL returns your page.

4. **Reach the user.**
   - Local session: `open <url>` (macOS) or `xdg-open <url>`.
   - Remote or SSH session with tailscale: `tailscale serve --bg <port>`, announce the https tailnet URL it prints. Tailnet-only is the default; escalate to `tailscale funnel` only when the user explicitly wants someone outside the tailnet to answer.
   - Remote without tailscale: hand the user `ssh -L <port>:127.0.0.1:<port> <host>` plus the localhost URL.
   Done when the URL is announced in chat.

5. **The round trip.** Wait for submits without burning attention: watch the listener's output for `SUBMIT ` lines (in Claude Code, Monitor the background task's output file until a new SUBMIT line lands; on agents without a watcher, `python3 serve.py --await <dir>` blocks until the next answer, and running it in the background makes its exit the wake-up). On each answer: read the JSON, act on it, rewrite `state.json` in place. Never restart the listener to change the page. When an answer asks a factual question, research it and put the findings in the next state. Done when the page's purpose is met: every planned screen answered, or the user closes it out in chat.

6. **Teardown.** Kill the listener. If tailscale was configured, remove it: `tailscale serve --https=443 off` (or `funnel --https=443 off`). Graduate durable conclusions to wherever the invoking task records them (ticket, doc, chat summary); the page itself is throwaway. Done when nothing listens and no serve config remains.

## Answers

`POST /submit` accepts any JSON; the listener stamps `ts` and appends it to `<dir>/answers.jsonl`. Give every screen a `qid` field so multi-question pages stay attributable. Anyone holding the URL can answer: treat submissions as the user's delegates, and include a name field in the form when it matters who answered.

## Safety

The page is reachable by whoever has the URL. Never render secrets, tokens, or private data you would not paste in a group chat; funnel means the public internet. Everything under `<dir>` is disposable once conclusions have graduated.
