---
name: doc-integrity
description: >
  Document anti-drift and verification: in a team / multi-agent setting, docs/ is the single source
  of truth, so the documents themselves must be continuously verified and must not drift from the
  code or from each other. Read this to confirm existing docs are still trustworthy, when closing a
  change, or when an agent takes over. Covers code↔doc bidirectional consistency, doc↔doc
  consistency, scriptable drift detection, and independent review.
---

# doc-integrity — document anti-drift & verification

> 語言 / Language: [繁體中文](doc-integrity.zh-tw.md) · **English**

## Purpose

Team / multi-agent collaboration treats `docs/` as the single source of truth — so **once the docs drift from reality (the code) or from each other, the whole governance collapses**: later agents make wrong decisions based on wrong docs. This file ensures docs are not merely "written" but **continuously verified and kept drift-free**.

## When to read

- To confirm whether existing `docs/` is still trustworthy (especially when taking over someone else's / another agent's project)
- When closing each change (verify doc consistency together with acceptance)
- During an agent's Session startup check

## Two kinds of consistency (both matter)

### 1. Code ↔ docs (vertical)
- If structural code changed (modules, data models, interfaces/APIs), `docs/structure/` must be synced; conversely, entities/modules/interfaces the docs describe must be findable in the code.
- Acceptance criteria (Guideline §7) must match actual behavior and tests.

### 2. Docs ↔ docs (horizontal)
- The four structures line up: logical modules ↔ directory folders ↔ design components ↔ data entities, with consistent names and boundaries.
- Every FR in the Guideline traces down to structure and some ACC; every CHG links back to an FR and forward to an ACC.

## Anti-drift trigger points

Not one-off, but embedded in the flow and checked repeatedly:
- **Change close-out**: when closing a CHG, also confirm structure docs are synced (per modification-guide's "documents are the truth").
- **On entry**: during the Session startup check, sweep doc consistency; fix drift before doing new work.
- **CI (optional)**: automate it as a PR gate via ci-cd's "structure-sync check".

## How to verify

- **Script what you can** (preferred — repeatable, unbiased):
  - `src/` changed structural paths (e.g. models/schema) but `docs/structure/` didn't → flag.
  - An entity/module name mentioned in docs can't be grepped in the code → flag (docs may be stale or names drifted).
  - Every CHG has a matching ACC; every FR appears in structure/ACC.
- **Independent review for the rest**: whether the meaning is still correct and the rationale still holds — give it to a non-author agent (see independent-acceptance).

## Document verification checklist

Each document should satisfy:
- [ ] has a version and date (you can tell new from old)
- [ ] traceable: links to its FR / CHG / ACC numbers
- [ ] consistent with the latest code (vertical)
- [ ] consistent with the other structure docs (horizontal)

## When you find drift

**Don't silently edit the doc** — return to `modification-guide` and add a "doc sync" change (or note it in the current CHG), stating the drift and the fix, to keep the trail. Drift itself is a signal worth recording: it means some earlier change failed to bring the docs along.
