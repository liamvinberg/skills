# Round-trip page recipes

Pick by the page's shape. State shapes are conventions, not schemas: extend freely, keep `qid` on anything submittable.

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

## Show-and-confirm

**When:** a plan, document, diff, or design needs sign-off, not discussion.

**Page:** the content rendered for reading, one confirm control (approve / request changes), one note field. Single submit, then a done state.

## Comparison picker

**When:** choosing between concrete alternatives: designs, copy variants, approaches, configurations.

**Page:** the options side by side or stacked, each previewed honestly (not described), radio or click-to-pick, note field, one submit. If options are visual, render them, do not screenshot-describe them.

## Parameter playground

**When:** tuning values where feel beats argument: animation timing, spacing, chart parameters, thresholds.

**Page:** sliders and inputs bound to a live preview (CSS variables, inline SVG, canvas). The preview is the point: it must update instantly on input. Submit sends the chosen values as JSON.

## Show-only

**When:** a visualization, walkthrough, report, or diagram that chat text would flatten. No answer needed.

**Page:** no submit control. Teardown after the user closes it out in chat.
