# Round-trip page recipes

Pick by the page's shape. Recipes run from pure show to pure ask; no recipe is the default. State shapes are conventions, not schemas: extend freely, keep `qid` on anything submittable. Recipes compose: an interview screen can carry product-true variations or a playground as its options, a sequence can end on a show-and-confirm, and a dashboard can grow a confirm control when a decision ripens.

## Show-only

**When:** a visualization, walkthrough, report, or diagram that chat text would flatten. No answer needed.

**Page:** no submit control. Teardown after the user closes it out in chat.

## Living dashboard

**When:** long-running work throws off state worth watching: a migration's progress, findings accumulating, a build-and-verify loop. The page is the session's second screen and lives as long as the work, not a single question.

**Page:** the work as it stands: counts, a findings table, what is running, what failed. No submit control by default; add one when a decision ripens (a stop control, a triage pick) and drop it from the next state once spent.

**Loop:** rewrite `state.json` at every meaningful step; the listener outlives any number of rewrites. Teardown when the work closes, not when the first view has been read.

## Architecture explorer

**When:** the user wants to understand how something works (a codebase, a system, a pipeline) and the honest answer is a map, not prose. The submit channel is navigation: each click asks you to go deeper.

**State:** the focused view plus the trail back out.

```json
{
  "qid": "explore", "focus": "payments", "title": "payments service",
  "trail": [ { "focus": "overview", "label": "system" } ],
  "body_html": "<p>what this piece is for, in two sentences</p>",
  "figure_html": "<svg>...the focused region, honestly drawn...</svg>",
  "targets": [ { "id": "ledger", "label": "ledger", "hint": "double-entry core" } ]
}
```

**Page:** a renderer over state.json: the focused view drawn as a figure, each target a clickable region or listed link, the `trail` as breadcrumbs climbing back out. A click submits `{ "qid": "explore", "target": "ledger" }`; there is no form.

**Loop:** fog of war over a codebase: draw deeper views only when asked, and read the real code before drawing it. Pre-rendering every depth defeats the recipe; the round trip is what keeps the map honest.

## Show-and-confirm

**When:** a plan, document, diff, or design needs sign-off, not discussion.

**Page:** the content rendered for reading, one confirm control (approve / request changes), one note field. Single submit, then a done state.

## Comparison picker

**When:** choosing between concrete alternatives: designs, copy variants, approaches, configurations.

**Page:** the options side by side or stacked, each previewed honestly (not described), radio or click-to-pick, note field, one submit. If options are visual, render them, do not screenshot-describe them.

## Product-true variations

**When:** the discussion is about the product's own UI and the session runs in the product's repo: show each variation as it would actually ship, in the product's real styles, instead of describing it or mocking it in the page's baseline.

**Page:** bring the product's styles in at full fidelity: link its built stylesheet, inline its tokens, or copy the component markup wholesale. Render each variation in its own scoped container, or an iframe when the product CSS is global and would bleed into the page chrome. Label each variation by what changes, put the pick control beneath, keep the page's own baseline for everything that is not the variation.

**Loop:** a pick plus note is an answer like any other. When a note proposes a tweak, render the tweak as a new variation in the next state rather than describing it back in words.

## Parameter playground

**When:** tuning values where feel beats argument: animation timing, spacing, chart parameters, thresholds.

**Page:** sliders and inputs bound to a live preview (CSS variables, inline SVG, canvas). The preview is the point: it must update instantly on input. Submit sends the chosen values as JSON.

## Sequential interview

**When:** many decisions resolved one at a time, later questions depend on earlier answers (fog of war), or answering is delegated to someone besides the invoker. This is the grilling delivery.

**State:** one live question at a time.

```json
{
  "qid": "q1-slug", "n": 1, "branch": "topic · 1 of N", "status": "open",
  "title": "The question, stated plainly",
  "body_html": "<p>context the answerer needs, nothing more</p>",
  "figure_html": "<table>...</table> or null",
  "recommendation": { "label": "the pick", "why": "one sentence" },
  "input": { "type": "choice", "options": [
    { "id": "a", "label": "...", "desc": "...", "recommended": true },
    { "id": "b", "label": "...", "desc": "..." } ], "note": true },
  "history": [ { "n": 1, "title": "...", "answer": "one-line gist" } ]
}
```

**Page:** a renderer over state.json. One decision per screen. The recommended option pre-selected and visibly tagged. A free-text note on every question (nuance beats another option). A route-so-far transcript from `history`. A quiet waiting state after submit. A done screen when `status` is `done`.

**Loop:** author the next question only after reading the answer; a rich note can reroute the remaining tree. Research mid-loop when an answer asks something factual, and present findings as the next screen's context. Keep every decision in `history` so the final synthesis writes itself.
