# Fan-out: parallel lanes

Rules for two or more lanes at once. A single lane needs none of this.

## Slice

- A lane carries a **chain**: tasks that depend on each other run
  sequentially in one lane — fresh worker per task, each committed
  (accepted) before the next spawns. Independent chains get their own lanes.
- Lane manifests — the union of each brief's file list — must be disjoint.
  Overlap found at plan time means re-slicing, not hoping the judge
  catches it.
- A dependency across lanes is a **wave** boundary: land every lane of the
  wave, then cut the next wave's lanes from the new tip.
- **Contract first.** Shared surface is yours, committed to base from the
  main tree before any lane is cut: types, interface stubs, new deps and
  their lockfile. Lanes branch from that commit; a dep change inside a lane
  is a scope violation. This is what makes disjoint manifests possible —
  and rebase conflicts rare.
- Cap concurrent lanes at ~4; queue the rest.

## Land

- Lanes land as they finish, one at a time — two interleaved landings race
  the base tip.
- After the last lane, run the full gate once on base: lanes green alone
  can still break composed, and only a post-merge run catches it.

Done when every lane is landed or reported failed, `git worktree list`
carries no lane of this run's, and the base gate is green.
