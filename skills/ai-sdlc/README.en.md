# ai-sdlc — AI Development Governance Skill Suite

> 語言 / Language: [繁體中文](README.md) · **English**

A set of skills that give the AI a consistent process to follow when assisting with development. The core idea: **capture requirements, structure, changes, and acceptance as documents first, then have the AI read those documents as its basis for later work** — instead of guessing from scratch every time.

This README is the entry point for the whole system. Before starting a development task, the AI should read here to decide "which skill applies right now".

## Why this process exists

The biggest problems with AI-assisted development are "amnesia" and "drift": every conversation lacks the context of prior decisions, so it's easy to make changes that conflict with the existing architecture. This process fixes each stage's output into a document (AI Guideline, structure docs, change records, acceptance reports), so any single AI task can read the docs first and then act, preserving consistency.

## Four stages and their skills

The whole thing is a closed loop: requirements come in, work proceeds to acceptance. **A failed acceptance is routed back to the modification flow to be redone and re-verified, until it passes or the user accepts**:

```
 [requirement / new feature]
      │
      ▼
 requirement-analysis ──► structure-design ──► implement ──► acceptance-verification
  (requirements→Guideline) (four structures)                        │
                                                          ┌──────────┴──────────┐
                                                        pass                   fail
                                                          │                      │
                                                          ▼                      ▼
                                                        done            modification-guide
                                                                   (mod guide + record + struct update)
                                                                              │
                                                                              ▼
                                                                  re-implement → re-verify
                                                                  (back to acceptance)

 Other entry: the user proposes a "modification / new feature" at any time
   → mandatory-load modification-guide → implement → acceptance-verification (same verify line)
```

`modification-guide` has two entry points: (1) a user-initiated modification/new feature, and (2) a failed acceptance routed back for fixes. Both go through "change governance → re-implement → re-verify", closing the loop so there's never a dead end where "acceptance failed but nobody picks it up".

| Stage | Skill | When to use | Main output |
|-------|-------|-------------|-------------|
| 1. Requirement analysis | `requirement-analysis` | New project/requirement; need to clarify what to build | `docs/ai-guideline.md` |
| 2. Structure design | `structure-design` | Guideline confirmed; need the system structure | `docs/structure/*.md` |
| 3. Change governance | `modification-guide` | A modification or new feature is proposed (**mandatory load**) | `docs/changes/*.md` + updated structure |
| 4. Acceptance | `acceptance-verification` | Implementation/change done; confirm it meets the bar | `docs/acceptance/*.md` |

## Mandatory-load rule (original requirement #5)

**Whenever the user proposes a "modification" or "new feature" within a session, the AI must first load and follow the `modification-guide` skill — it may not be skipped.** This is because any change can touch existing structure and prior decisions; skipping change governance causes architectural drift and missing records. The detailed mechanism is in `modification-guide/SKILL.md`.

The other skills are read "on demand, not mandatory": the AI determines which stage the current task belongs to, and only then reads the corresponding skill, avoiding loading large amounts of irrelevant content at once.

## Document storage convention

The documents this suite produces live under the **target project's** `docs/` (not in this repo). This repo only stores the skills themselves. Suggested layout:

```
<target-project>/
└── docs/
    ├── ai-guideline.md          # from requirement analysis
    ├── structure/
    │   ├── directory.md          # directory structure
    │   ├── logical.md            # logical structure
    │   ├── design.md             # design structure
    │   └── data.md               # data structure
    ├── changes/
    │   └── CHG-YYYYMMDD-NN.md    # one record per change
    └── acceptance/
        └── ACC-YYYYMMDD-NN.md    # one report per acceptance
```

If the target project already has another documentation convention, follow that project's, and note the actual paths in the AI Guideline.

## Operating principles

1. **Read before doing**: before acting, read the relevant stage's skill and the existing documents.
2. **Documents are the truth**: structure docs and the Guideline are the basis for later decisions; if the structure changes, the docs must be updated in sync — you can't change only the code.
3. **Leave a trace for every change**: a modification must always leave a record under `docs/changes/`, stating motivation and trade-offs.
4. **Acceptance aligns to source**: acceptance criteria come from the Guideline and the change's mod guide — never invented on the spot.

## Sub-skills

- [`requirement-analysis/`](requirement-analysis/SKILL.en.md) — requirement analysis, produces the AI Guideline
- [`structure-design/`](structure-design/SKILL.en.md) — produces directory/logical/design/data structures
- [`modification-guide/`](modification-guide/SKILL.en.md) — mod guide, change records, structure updates, mandatory load
- [`acceptance-verification/`](acceptance-verification/SKILL.en.md) — verify against acceptance results
