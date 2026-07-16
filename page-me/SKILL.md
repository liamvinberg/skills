---
name: page-me
description: Explicit invocation only. Use only after the user types `page-me`, `$page-me`, or `/page-me` as the requested skill in the current request. Never activate from task content alone, including requests for pages, forms, sliders, interactive content, visualizations, secret fields, or outside answerers. Once invoked, communicate through a locally served round-trip HTML page that can show interactive content or collect structured answers whose submissions flow back into the session.
---

A **round-trip page** is a single-file HTML page served by a long-lived local listener, wired to the session in both directions: you rewrite its state and the page re-renders without a reload or a listener restart; the user submits and the answer lands back in the session. A page can **show** (explain, visualize, keep a live surface current), **ask** (collect structured answers), or do both; the wiring is identical either way.

## Delivery contract

Explicit invocation is a hard precondition. Never self-initiate this skill, even when rendering would improve the material, a submission must stay out of the transcript, or the answerer is someone besides the invoker. If the user did not name `page-me` in the current request, do not apply any part of this workflow. If an asking page is used, never hand over its URL and end the turn. Arm a wake-capable await before announcing the URL, keep the turn alive while waiting, process each submit, update the page, and re-arm the await. A listener left running in an unread PTY is not monitoring. Tailscale solves reach, not wake-up. If the harness cannot wake the agent from a submission, fall back to chat.

## Steps

1. **Workspace.** Create a fresh directory per page: the project's own throwaway-prototype location if its conventions name one (e.g. a gitignored `scratchpad/`), else `/tmp/html-comm/<slug>/`. If the name is already taken, pick another — two pages must never share a directory, or their answer logs interleave. Done when the directory exists outside version control.

2. **Author.** Pick the recipe matching the page's shape in [PATTERNS.md](PATTERNS.md) before writing anything. Copy `assets/template.html` to `<dir>/index.html` and replace its REPLACE markers, keeping the helpers. Static content lives in the HTML; anything that updates lives in `<dir>/state.json` and renders through `watchState`. The template's baseline is the entire theme: add no hue, no fonts, no decoration, and keep wide content scrolling inside its own container. Done when index.html renders your content with the helpers intact.

3. **Listen.** Run `python3 <skill>/assets/serve.py <dir>` in the background and parse the printed `LISTENING http://127.0.0.1:<port>` line. One listener serves the page for its whole life, across any number of submits and state rewrites. Done when fetching the URL returns your page.

4. **Reach the user.** The page must be reachable by whoever it is for. Private reach is the default; expose the page publicly only when the user explicitly asks for an outside answerer. When the project or user configuration names a reach mechanism for remote sessions, prefer it.
   - Local session: `open <url>` (macOS) or `xdg-open <url>`.
   - Remote session: serve through the environment's private tunnel. With tailscale: `tailscale serve --bg --https=<port> <port>` — reusing the listener's own port number keeps concurrent pages from contending, where a bare `serve --bg <port>` claims the machine URL's root and silently evicts whichever page held it. Announce the https `:<port>` tailnet URL it prints. Escalate to `tailscale funnel` only on that explicit ask; funnel permits only ports 443, 8443, and 10000, so remount on a free one of those first. The universal fallback is handing the user `ssh -L <port>:127.0.0.1:<port> <host>` plus the localhost URL.
   Done when the URL is announced in chat.

5. **The round trip.** A page that only shows has nothing to wait for: rewrite `state.json` whenever the session teaches the page something new, and move to teardown once the user closes it out in chat. A page that asks is not ready to announce until its first wake-up await is armed. Use a background file-watch or monitor filtered to `^SUBMIT ` when the harness provides one. Otherwise run `python3 serve.py --await <dir> --after <answer-count>` and attach a yielded or deferred wait whose completion wakes the same turn; in Codex, do not send the final response while that wait is armed. On each answer: read the JSON, act on it, rewrite `state.json` in place, then re-arm with the new answer count before returning control. Never rely only on unread listener output, and never restart the listener to change the page. When an answer asks a factual question, research it and put the findings in the next state. Done when the page's purpose is met: every planned screen answered, or the user closes it out in chat.

6. **Teardown.** Kill the listener. If a tunnel was configured, remove only your page's mount (tailscale: `tailscale serve --https=<port> off`, or `funnel --https=<port> off`) — other sessions may hold mounts of their own. Graduate durable conclusions to wherever the invoking task records them (ticket, doc, chat summary); the page itself is throwaway. Done when nothing listens and no serve config remains.

## Answers

`POST /submit` accepts any JSON; the listener stamps `ts` and appends it to `<dir>/answers.jsonl`. Give every screen a `qid` field so multi-question pages stay attributable. Anyone holding the URL can answer: treat submissions as the user's delegates, and include a name field in the form when it matters who answered.

## Safety

The page is reachable by whoever has the URL. Never render secrets, tokens, or private data you would not paste in a group chat; a public tunnel is the public internet. Everything under `<dir>` is disposable once conclusions have graduated.
