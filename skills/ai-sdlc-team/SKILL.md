---
name: ai-sdlc-team
description: >
  AI development governance (team edition, self-contained): covers the full flow — requirement
  analysis → structure design → modification governance → acceptance — plus anti-drift, a subagent
  worklog and error knowledge base, optional CI/CD, and team collaboration (cross-agent handoff /
  parallel work, independent acceptance, roles and read/write permissions). Use when a project is
  developed by several people or multiple AI agents sequentially or in parallel, needs drift-free
  handoff, and independent gating. "Team" is not limited to humans; it can be an AI-agent team. This
  edition is self-contained — the solo ai-sdlc skill is not required.
---

# ai-sdlc-team — AI development governance (team edition, self-contained)

> 語言 / Language: [繁體中文](SKILL.zh-tw.md) · **English**

Gives the AI a consistent development process and supports **multi-person / multi-AI-agent collaboration**. Core idea: **capture requirements, structure, changes, and acceptance as documents, and everyone (including your future self and other agents) reads the docs as the basis** — not individual conversation memory. **This edition is self-contained: it covers full governance + collaboration and does not require the solo `ai-sdlc` skill** (for plain individual work, the lighter `ai-sdlc` is an option).

## "Team" is not limited to humans — it can be an AI-agent team

"Team" means **multiple independent execution units**: several developers, multiple AI agents (different instances / contexts), or a mix. They can't share conversation memory, so they collaborate only through `docs/`; and the independence from separating the "implementing agent" and the "verifying agent" is how quality is gated.

## The closed loop

```
 [requirement / new feature]
      │
      ▼
 requirement analysis ──► structure design ──► implement ──► acceptance
 (Guideline)              (four structures)                  │
                                                    ┌────────┴────────┐
                                                  pass             fail
                                                    │                │
                                                    ▼                ▼
                                                  done    modification governance → re-implement → re-verify
```

## Stage guides (load as needed)

| Stage | When to use | Guide |
|-------|-------------|-------|
| 1. Requirement analysis | new project/requirement | [`references/requirement-analysis.md`](references/requirement-analysis.md) |
| 2. Structure design | Guideline confirmed; define structure | [`references/structure-design.md`](references/structure-design.md) |
| 3. Modification governance | a modification/new feature is proposed (**mandatory**) | [`references/modification-guide.md`](references/modification-guide.md) |
| 4. Acceptance | implementation/change done | [`references/acceptance-verification.md`](references/acceptance-verification.md) |

## Cross-cutting guides

| Aspect | When to use | Guide |
|--------|-------------|-------|
| Document anti-drift & verification | confirm docs are trustworthy; at close-out; on takeover | [`references/doc-integrity.md`](references/doc-integrity.md) |
| Subagent worklog + error knowledge base | before dispatching subagents, or before a dispatched run | [`references/agent-worklog.md`](references/agent-worklog.md) |
| CI/CD integration (**optional**) | automate gates as pre-commit or pipeline | [`references/ci-cd.md`](references/ci-cd.md) |

## Team collaboration guides

| Aspect | When to use | Guide |
|--------|-------------|-------|
| Cross-agent collaboration / handoff | handoff, cross-session accumulation, concurrent multi-agent | [`references/cross-agent.md`](references/cross-agent.md) |
| Cross-agent / multi-scenario independent acceptance | code done; verified by a different, read-only agent across scenarios | [`references/independent-acceptance.md`](references/independent-acceptance.md) |

## Mandatory rule: changes always go through governance first

Whenever someone proposes a "modification" or "new feature", **go through `modification-guide` first; do not edit code directly**; once implemented, **close acceptance in the same round** (produce the ACC, backfill CHG status) — don't hand acceptance off to the next session (nobody picks it up).

## Session startup check (required across sessions / handoffs)

On every entry, before any new requirement, scan: any non-Accepted CHG under `docs/changes/`, any missing ACC under `docs/acceptance/`, and the known pitfalls in `docs/knowledge/` — close what's pending and read the knowledge base, then start.

## Document storage convention

Outputs live under the **target project's** `docs/`: `ai-guideline.md`, `structure/{directory,logical,design,data}.md`, `changes/CHG-*.md`, `acceptance/ACC-*.md`, `worklog/`, `knowledge/errors.md`. **Across projects**, note each doc's owning "Project" in the header and prefix ids with the project.

## Operating principles

1. **Every agent has an explicit role and read/write permission**: when dispatching (human or AI agent), define "role + readable/writable scope"; the verifier is **read-only** (reads code & criteria, writes only its ACC, never edits the code under review). Least privilege.
2. **Subagents write before executing, record errors then continue**: a subagent writes "what I'm doing" in the worklog before acting; on error records "what + root cause + fix" then continues; reports its error list on completion, which the parent consolidates into the knowledge base.
3. **Read docs/ on entry (incl. the knowledge base)**: don't rely on memory; the docs win when they disagree (resilient to compaction/handoff).
4. **Leave a clean state on exit**: close acceptance, backfill status, sync structure docs.
5. **Claim before parallel work**: claim non-overlapping scope (with role and R/W) in the coordination file; single-writer rule.
6. **Acceptance is independent, multi-scenario, read-only**: not self-verified by the implementer.
7. **Docs resist drift**: sync structure on change; when drift is found, record the fix back through the flow.
8. **Automate where you can (optional)**: with CI/CD, place gates in pre-commit / pipeline.
