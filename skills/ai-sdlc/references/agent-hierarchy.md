---
name: agent-hierarchy
description: >
  Agent hierarchy and org: how multiple agents are organized into a managed hierarchy — each agent
  has an ID + a fixed role and task scope and may not exceed its remit; a sub-agent may spawn its own
  sub-agents within its scope (recursive), but permission can only narrow, never widen, and the
  parent actively manages it; the typical chain is analysis → implementation (a lead implementer
  dispatches sub-agents and self-checks) → independent acceptance. Read this when a task is split
  across multiple agents, or when an agent needs to dispatch sub-agents.
---

# agent-hierarchy — agent hierarchy & org

> 語言 / Language: [繁體中文](agent-hierarchy.zh-tw.md) · **English**

## Purpose

Turn "several agents working together" into a **chartered, bounded, managed** hierarchy rather than a swarm of agents running loose. Core: **every agent is numbered and granted a fixed task and scope, and may not do anything outside it**; when more capacity is needed it can spawn sub-agents, but **the parent actively manages them and permission can only narrow, never widen**.

## When to read

- A task is to be split across multiple agents (e.g. analysis / implementation / acceptance)
- An agent has a large workload and needs to dispatch sub-agents

## Org principles

1. **ID + fixed role + fixed scope**: every agent has a unique ID, a fixed role, a fixed task scope, and read/write permission. Name them to reflect the hierarchy: `A1` (analysis), `I1` (lead implementer), `I1.1`/`I1.2` (I1's implementation sub-agents), `V1` (verifier).
2. **No exceeding the remit**: an agent does only its assigned task and reads/writes only its granted scope. **Need to do something out of scope → report to the parent**, who decides (reassign / widen the grant); **never self-expand.**
3. **Recursive delegation, permission only narrows**: a sub-agent may spawn its own sub-agents within its own granted scope, but:
   - the scope it grants downward **must be a subset of its own** (permission cannot widen);
   - the whole chain (ID, role, scope, parent-child) is registered in the coordination file;
   - **the parent actively manages**: assign, track, converge — don't let them run loose.
4. **Parent's duties**: assign tasks → track progress → confirm and verify sub-agents' output → converge/aggregate → record errors into the knowledge base (see agent-worklog).

> Applicability: **solo or team**. A solo user with an AI that spawns sub-agents can use this org too (analysis/implementation/acceptance are all AI sub-agents); you are the top-level manager.

## Recursive creation depends on the AI mechanism (important)

Whether "a sub-agent can spawn its own sub-agents" is possible **depends on the underlying AI platform/mechanism supporting nested sub-agents** — some mechanisms only let the top level dispatch sub-agents, and sub-agents can't dispatch further. So:

- **If nesting is allowed**: proceed with "recursive delegation, permission narrows only + active parent management" above.
- **If nesting is not allowed (single-level dispatch only)**: fall back to an equivalent outcome —
  - the **top-level agent directly creates all needed agents** (flat org), acting as everyone's parent; or
  - that agent **does the sub-tasks itself, in sequence** (no further dispatch), then reports.
- **Regardless of depth, these don't change**: IDs, fixed scope, no exceeding the remit, org registry, parent management, implementer-doesn't-self-verify. **Only the "hierarchy depth" is limited by platform capability**; the governance principles hold.

On entry, check whether the current mechanism supports nesting; if unsure, use a flat org — it's the safest.

## Typical chain (implementation scenario)

```
A1 analysis ──► I1 lead implementer ──► V1 independent acceptance
                ├─ I1.1 sub-impl (module X)
                └─ I1.2 sub-impl (module Y)
```

1. **Analysis agent (A1)**: produces Guideline / structure / impact analysis from the requirement — **analysis only, no implementation**.
2. **Lead implementer (I1)**: from A1's analysis, splits implementation into sub-tasks and dispatches them to **implementation sub-agents (I1.1, I1.2…)**; each does only its assigned module and writes only that module's scope.
3. **I1 confirms and verifies** each sub-agent's output (integrate, run tests, check consistency); aggregates once all sub-tasks are done.
4. **Only after all implementation is complete**, hand off to an **independent verifier (V1)** — V1 ≠ any agent in the implementation chain, and **read-only** — for multi-scenario acceptance, producing the ACC (see independent-acceptance).
5. Iron rules: **I1 does not self-verify** (player can't be referee); **V1 does not edit code** (found a problem → back to modification-guide for the implementation chain to fix).

## Org registry (coordination file)

Maintain the org table in `docs/coordination.md` so anyone/any agent can see who does what and who manages whom:

```markdown
# Agent org
| ID   | Role | Parent | Task / scope | R/W permission | Status |
|------|------|--------|--------------|----------------|--------|
| A1   | analysis | —  | requirement/structure/impact | docs/ + read code | done |
| I1   | lead impl | — | coordinate impl, integrate | RW src/ | in progress |
| I1.1 | sub-impl | I1 | module X | RW src/x | in progress |
| I1.2 | sub-impl | I1 | module Y | RW src/y | done |
| V1   | verifier | — | multi-scenario acceptance | read-only + write docs/acceptance | standby |
```

## Relation to the rest of the flow

- Extends `cross-agent` (roles/permissions/claim): adds **ID + hierarchy + recursive delegation (narrow-only) + active parent management**.
- Extends `agent-worklog`: each numbered agent writes a worklog on entry; reports errors up; the parent consolidates them into the knowledge base.
- Extends `independent-acceptance`: when the implementation chain (I1 and its children) is done → hand off to an independent V1; the implementer never self-verifies.
- Maps to ai-sdlc stages: A1 ≈ requirement analysis / structure design; the I1 chain ≈ modification governance + implementation; V1 ≈ acceptance.
