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

Team collaboration works only if every agent / person writes state and decisions into `docs/` and reads it on entry — rather than relying on individual conversation memory (which can't cross units and gets compacted). This continues ai-sdlc's "documents are the truth / don't rely on memory" principle, promoting it from "personal memory" to "team collaboration medium". **For exactly this reason, the documents themselves must be drift-resistant and continuously verified** (see doc-integrity).

## References (load as needed)

| Aspect | When to read | Guide |
|--------|--------------|-------|
| Cross-agent collaboration / handoff | work hands off, accumulates across sessions, or multiple agents touch the same project | [`references/cross-agent.md`](references/cross-agent.md) |
| Document anti-drift & verification | confirm existing docs are trustworthy; at change close-out; on takeover | [`references/doc-integrity.md`](references/doc-integrity.md) |
| Cross-agent / multi-scenario independent acceptance | when code is done and acceptance is due (run by a different agent, different scenarios) | [`references/independent-acceptance.md`](references/independent-acceptance.md) |
| CI/CD integration (**optional**) | project has/adopts CI/CD; want acceptance & structure-consistency as PR gates | [`references/ci-cd.md`](references/ci-cd.md) |

In short: `cross-agent` covers **sequential handoff** and **parallel multi-agent**; `doc-integrity` keeps **docs from drifting** from code or each other; `independent-acceptance` requires **verifier ≠ implementer, across scenarios**; `ci-cd` (optional) automates those gates. Projects without a pipeline skip ci-cd and rely on the flow.

## Operating principles (on top of ai-sdlc's)

1. **Read docs/ on entry**: before any agent takes over, read existing docs to restore state (including ai-sdlc's Session startup check).
2. **Leave a clean state on exit**: close acceptance in the same round, backfill status, sync structure docs, so the next agent can continue just by reading docs.
3. **Claim before parallel work**: when multiple agents work at once, claim non-overlapping scope in the coordination file first; the single-writer rule avoids overwrites.
4. **Acceptance must be independent and multi-scenario**: when code is done, it is **not self-verified by the implementing agent** — a different agent runs verification under different scenarios, then aggregates (see independent-acceptance).
5. **Verify docs, resist drift**: documents aren't just written — continuously verify they're consistent with the code and with each other; when drift is found, record the fix back through the flow (see doc-integrity).
6. **Automate where you can (optional)**: with CI/CD, turn acceptance, structure-sync, and change traceability into machine gates rather than relying on discipline.
