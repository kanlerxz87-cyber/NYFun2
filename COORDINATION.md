# COORDINATION.md

Shared task board for parallel agent sessions. Read before starting. Claim a task by writing your session ID and file scope, then commit and push the claim immediately. Never start a task another session has claimed.

## Session Log

| Timestamp (UTC) | Session ID | Action | Notes |
|---|---|---|---|
| 2026-11-25T00:00:00Z | s096f8cf2 | Session started | Branch `arena/096f8cf2-nyfun2` from `a3a2848`. Repo initially contained only README.md. No other active claims observed. |

## Task Board

| Task | Status | Owner | Scope (files/dirs) | Started | Last update | Notes |
|---|---|---|---|---|---|---|
| Coordination/bootstrap | in progress | s096f8cf2 | `COORDINATION.md` | 2026-11-25 | 2026-11-25 | Initial setup. |
| Research: Michelin restaurants NYC (official) | in progress | s096f8cf2 | `data/michelin-restaurants.*`, `docs/research/michelin.*` | 2026-11-25 | 2026-11-25 | Verify against official Michelin Guide. Record edition/date. |
| Research: Hotels near Michelin clusters (verified pricing) | in progress | s096f8cf2 | `data/hotels.*`, `docs/research/hotels.*` | 2026-11-25 | 2026-11-25 | Real verified pricing only; flag unverified. |
| Research: Activities/restaurants social links & hours | in progress | s096f8cf2 | `data/activities.*`, `docs/research/activities.*` | 2026-11-25 | 2026-11-25 | Official links + social media links; hours from official sources. |
| Site build (GitHub Pages) | in progress | s096f8cf2 | `docs/`, `index.html`, `assets/`, `.nojekyll` | 2026-11-25 | 2026-11-25 | Clean mobile-friendly dashboard/site. |
| Executive summary & decision questions | in progress | s096f8cf2 | `docs/executive-summary.*`, `docs/decision-questions.*` | 2026-11-25 | 2026-11-25 | No hallucinations; flag unknowns. |
| Verification & flagged review | in progress | s096f8cf2 | `docs/verification.*`, `docs/flagged-review.*` | 2026-11-25 | 2026-11-25 | Line-by-line verification log. |
| Integration/publish | unclaimed | - | site index/nav/shared data | - | - | Final integration only after all tasks done; re-verify. |

## Rules (from task brief)

- Claim before starting; commit and push claim immediately.
- Never start a task another session has claimed.
- Non-overlapping scopes; each session uses `session-<id>/<task>` branch/worktree if splitting.
- Do not edit files owned by another session; log request here.
- Small frequent commits; `git pull --rebase` before every push.
- On merge conflict: stop, resolve without discarding other work, log it.
- When finished: record sources, verification performed, irregularities; mark done.
- Never mark verified without checking official source; link source.
- Shared outputs (table data, site index/nav) changed only by final integration session.
- Stale claim (>60 min, no commits) may be taken over with handoff note.
