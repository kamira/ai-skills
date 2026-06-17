---
name: ai-sdlc-team
description: >
  The team edition of ai-sdlc: on top of the solo ai-sdlc flow (requirement analysis → structure
  design → modification governance → acceptance), it adds multi-agent / multi-session collaboration
  and optional CI/CD integration. Use this when one project is developed by multiple AI agents, or
  by several people / sessions sequentially or in parallel, when work must hand off without drift,
  when parallel conflicts must be avoided, or when you want to wire document governance into CI/CD
  gates; read the references as needed — cross-agent for collaboration/handoff, ci-cd for CI/CD
  integration (optional). Assumes the project already uses ai-sdlc's document governance (docs/ as
  the single source of truth).
---

# ai-sdlc-team — AI development governance (team edition)

> 語言 / Language: [繁體中文](SKILL.zh-tw.md) · **English**

This is the **team extension layer** for [`ai-sdlc`](../ai-sdlc/SKILL.md). The solo edition handles "one person / one agent turning requirements into document-governed work"; the team edition handles "**how multiple agents / people collaborate without drift, hand off cleanly, and gate via CI/CD**".

## Solo vs team

- **ai-sdlc (solo)**: the core four stages — requirement analysis (AI Guideline), structure design (four structures), modification governance (change records), acceptance (report + re-fix loop). For one person or a single agent.
- **ai-sdlc-team (this skill)**: assumes ai-sdlc is in use and **additionally** handles two collaboration concerns — cross-agent collaboration/handoff, and (optional) wiring governance into CI/CD.

> This skill does not restate the four stages; for stage details read ai-sdlc's references. This skill focuses on the "collaboration layer" and the "automated-gating layer".

## "Team" is not limited to humans — it can be an AI-agent team

"Team" here means **multiple independent execution units**: several developers, or **multiple AI agents** (different instances / different contexts), or a mix. Multi-agent collaboration is the core scenario of this skill: agents can't share conversation memory, so they collaborate only through `docs/`; and the independence from separating the "implementing agent" and the "verifying agent" is exactly how the team edition gates quality.

## Premise: docs/ is the team's single source of truth

Team collaboration works only if every agent / person writes state and decisions into `docs/` and reads it on entry — rather than relying on individual conversation memory (which can't cross units and gets compacted). This continues ai-sdlc's "documents are the truth / don't rely on memory" principle, promoting it from "personal memory" to "team collaboration medium".

## Split with the base ai-sdlc

**Anti-drift (doc-integrity) and CI/CD (optional) live in the base `ai-sdlc`** (shared by solo and team, so they sit in the base); this team edition adds only the two "collaboration layer" concerns. Use it together with `ai-sdlc`.

| Aspect | When to read | Guide |
|--------|--------------|-------|
| Cross-agent collaboration / handoff | work hands off, accumulates across sessions, or multiple agents touch the same project | [`references/cross-agent.md`](references/cross-agent.md) |
| Cross-agent / multi-scenario independent acceptance | when code is done and acceptance is due (different agent, different scenarios) | [`references/independent-acceptance.md`](references/independent-acceptance.md) |
| Document anti-drift & verification | (in the base) confirm docs are trustworthy; at close-out; on takeover | `ai-sdlc`'s `references/doc-integrity` |
| CI/CD integration (**optional**) | (in the base) automate the gates per need | `ai-sdlc`'s `references/ci-cd` |

In short: `cross-agent` covers **sequential handoff** and **parallel multi-agent**, and requires every agent to carry an **explicit role and read/write permission**; `independent-acceptance` requires **verifier ≠ implementer, across scenarios, and the verifier is read-only**. Use the base ai-sdlc's references for anti-drift and CI/CD.

## Operating principles (on top of ai-sdlc's)

1. **Every agent has an explicit role and read/write permission**: when dispatching work (human or AI agent), define "role + readable/writable scope" up front — e.g. the implementer may write within its claimed scope; the verifier is **read-only** (may read the code and criteria, may write only its own ACC, must not edit the code under review). Permission separation is the basis of independence and of preventing accidental edits.
2. **Read docs/ on entry**: before any agent takes over, read existing docs to restore state (including ai-sdlc's Session startup check).
3. **Leave a clean state on exit**: close acceptance in the same round, backfill status, sync structure docs, so the next agent can continue just by reading docs.
4. **Claim before parallel work**: when multiple agents work at once, claim non-overlapping scope (with role and read/write scope) in the coordination file first; the single-writer rule avoids overwrites.
5. **Acceptance must be independent, multi-scenario, read-only**: when code is done, it is **not self-verified by the implementing agent** — a read-only verifier agent runs verification under different scenarios, then aggregates (see independent-acceptance).
6. **Anti-drift and automation**: keep docs verified and drift-free (use the base ai-sdlc's doc-integrity); with CI/CD, automate the gates (base ci-cd, optional).
