---
name: ai-sdlc
description: >
  AI development governance suite that splits work into four documented stages — requirement
  analysis, structure design, modification governance, and acceptance — so every AI task reads
  the docs first and stays consistent and traceable. Use this whenever the user plans a new
  project or feature, clarifies requirements, designs system architecture or a database,
  proposes any modification or new feature, or wants to verify whether results meet the bar;
  follow the staged flow and read the matching guide under references. Covers producing an AI
  Guideline, the four structures (directory/logical/design/data), change records with impact
  analysis, and acceptance reports with a re-fix loop. Important: as soon as the user proposes
  a modification or new feature, go through modification governance first rather than editing
  code directly.
---

# ai-sdlc — AI Development Governance

> 語言 / Language: [繁體中文](SKILL.zh-tw.md) · **English**

This skill gives the AI a consistent process when assisting with development. Core idea:
**capture requirements, structure, changes, and acceptance as documents first, then read those
documents as the basis for later work** — instead of guessing from scratch each time. Before
acting, read here to decide "which stage applies now", then read the matching guide under
`references/`.

## Why this is needed

The biggest problems with AI-assisted development are amnesia and drift: each conversation
lacks the context of prior decisions, so it's easy to make changes that conflict with the
existing architecture. This process fixes each stage's output into a document (AI Guideline,
structure docs, change records, acceptance reports) so any single task reads the docs first,
then acts.

## Four stages and their guides

```
 [requirement / new feature]
      |
      v
 requirement analysis --> structure design --> implement --> acceptance
 (Guideline)              (four structures)                  |
                                                    +--------+--------+
                                                  pass             fail
                                                    |                |
                                                    v                v
                                                  done       modification governance
                                                          (mod guide + record + struct sync)
                                                                  |
                                                                  v
                                                   re-implement --> re-verify (back to acceptance)

 Other entry: the user proposes a "modification / new feature" at any time
   --> mandatory modification governance --> implement --> acceptance
```

| Stage | When to use | Guide | Main output |
|-------|-------------|-------|-------------|
| 1. Requirement analysis | New project/requirement; clarify what to build | [`references/requirement-analysis.md`](references/requirement-analysis.md) | `docs/ai-guideline.md` |
| 2. Structure design | Guideline confirmed; define system structure | [`references/structure-design.md`](references/structure-design.md) | `docs/structure/*.md` |
| 3. Modification governance | A modification/new feature is proposed (**mandatory**) | [`references/modification-guide.md`](references/modification-guide.md) | `docs/changes/*.md` + updated structure |
| 4. Acceptance | Implementation/change done; confirm it meets the bar | [`references/acceptance-verification.md`](references/acceptance-verification.md) | `docs/acceptance/*.md` |

Read only the reference for the current stage to avoid loading irrelevant content at once.

## Mandatory rule: changes always go through governance first

**Whenever the user proposes a "modification" or "new feature" within a session, you must first
read and follow `references/modification-guide.md` — do not edit code directly.** Any change can
touch existing structure and prior decisions; skipping governance causes architectural drift and
missing records. Modification governance has two entry points: (1) a user-initiated change, and
(2) a failed acceptance routed back for fixes — both go through "governance -> re-implement ->
re-verify", closing the loop.

## Document storage convention

Outputs live under the **target project's** `docs/` (not this skill):

```
target-project/docs/
├── ai-guideline.md          # from requirement analysis
├── structure/{directory,logical,design,data}.md   # from structure design
├── changes/CHG-YYYYMMDD-NN.md                      # one per change
└── acceptance/ACC-YYYYMMDD-NN.md                   # one per acceptance
```

If the target project already has a documentation convention, follow that and note the actual
paths in the AI Guideline.

## Operating principles

1. **Read before doing**: read the stage guide and existing docs before acting.
2. **Documents are the truth**: if the structure changes, update the structure docs in sync.
3. **Trace every change**: a modification always leaves a record under `docs/changes/`.
4. **Acceptance aligns to source**: criteria come from the Guideline and the change's mod guide.
