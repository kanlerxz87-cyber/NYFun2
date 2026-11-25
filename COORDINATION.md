# COORDINATION.md

Shared task board for parallel agent sessions. Read before starting. Claim a task by writing your session ID and file scope, then commit and push the claim immediately. Never start a task another session has claimed.

## Session Log

| Timestamp (UTC) | Session ID | Action | Notes |
|---|---|---|---|
| 2026-11-25T00:00:00Z | s096f8cf2 | Session started | Branch `arena/096f8cf2-nyfun2` from `a3a2848`. Repo initially contained only README.md. No other active claims observed. |
| 2026-11-25T00:30:00Z | s096f8cf2 | Bootstrap committed | Created COORDINATION.md, docs scaffold, initial pages. |
| 2026-11-25T00:45:00Z | s096f8cf2 | Site/data draft committed | Added Michelin 2025 roster table, hotel framework, activities scaffold, decision questions, suggestions, verification/flags. Many required fields remain unverified and flagged. |

## Task Board

| Task | Status | Owner | Scope (files/dirs) | Started | Last update | Notes |
|---|---|---|---|---|---|---|
| Coordination/bootstrap | done | s096f8cf2 | `COORDINATION.md` | 2026-11-25 | 2026-11-25 | Created and maintained. |
| Research: Michelin restaurants NYC (official) | in progress | s096f8cf2 | `docs/michelin.html`, `docs/research/` | 2026-11-25 | 2026-11-25 | Verified names/stars/cuisines/Michelin URLs from official 2025 ceremony article. Social/hours/cost/official website fields unverified and flagged. 2026 selection recheck needed. |
| Research: Hotels near Michelin clusters (verified pricing) | needs review | s096f8cf2 | `docs/hotels.html`, `docs/research/` | 2026-11-25 | 2026-11-25 | Verification-ready shortlist and capture methodology created. **No live 2027 7-night pricing captured**; all pricing unverified. Requires live official capture with timestamps. |
| Research: Activities/restaurants social links & hours | needs review | s096f8cf2 | `docs/activities.html`, `docs/michelin.html` | 2026-11-25 | 2026-11-25 | Curated activities have official site links; social/hours/cost mostly unverified. Michelin rows include required columns but unverified values flagged. |
| Site build (GitHub Pages) | in progress | s096f8cf2 | `docs/`, `index.html`, `README.md`, `.nojekyll` | 2026-11-25 | 2026-11-25 | Static mobile-friendly site created in `docs/`. Needs GitHub Pages config (serve from `/docs`) and further data verification. |
| Executive summary & decision questions | done | s096f8cf2 | `docs/executive-summary.html`, `docs/decision-questions.html` | 2026-11-25 | 2026-11-25 | Drafted with knowns/unknowns/discovery steps. |
| Verification & flagged review | in progress | s096f8cf2 | `docs/verification.html` | 2026-11-25 | 2026-11-25 | Verification log and flagged review published. High-severity open flags remain. |
| Suggestions | done | s096f8cf2 | `docs/suggestions.html` | 2026-11-25 | 2026-11-25 | Suggestions-only section; no implementation. |
| Integration/publish | unclaimed | - | site index/nav/shared data | - | - | Final integration only after all tasks done; re-verify. Requires GitHub Pages enablement in repo settings (manual/authorized). |

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

## Handoff / Open Flags

- **HIGH**: Live hotel 7-night pricing for 2027 dates not captured. Requires official booking capture with timestamp, taxes/fees, cancellation, room type confirmation.
- **HIGH**: Social media links, open days/hours/exceptions, and cost-for-2-adults not verified for most listed restaurants/activities. Fields intentionally blank/flagged.
- **HIGH**: Transit matrix (hotel-to-venue ≤1h subway/bus) not computed.
- **MEDIUM**: Michelin edition is NYC 2025 ceremony article; recheck for 2026/2027 updates before travel.
- **MEDIUM**: Some listed restaurants are outside NYC (Blue Hill at Stone Barns, La Bastide by Andrea Calstier); confirm day-trip intent.
