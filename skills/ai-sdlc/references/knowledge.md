---
name: knowledge
description: >
  Knowledge base governance: record "errors hit during execution", "user correction directives",
  and "AI-observed recurring patterns" (autonomous shallow records that promote to deep after
  repeated uncorrected use) so the AI doesn't repeat mistakes or re-ask settled things; when a
  rule is updated, overwrite in place (no contradictory duplicates); the knowledge base is a
  high-priority rule set with an INDEX for scoped retrieval — read the index and load only the
  entries in scope, never the whole file. Read this when you receive a correction, when the same
  need/purpose recurs across CHGs/requirements, before entry, or when a request conflicts with a
  known rule. Distinction: requirement changes go through modification-guide; rules live here.
---

# knowledge — error & correction-directive knowledge base

> 語言 / Language: [繁體中文](knowledge.zh-tw.md) · **English**

## Purpose

The knowledge base is the durable memory that keeps the AI from repeating the same mistakes. Two entry types:

- **error**: technical errors hit during execution and their fixes (from agent-worklog).
- **directive (DIR)**: an **explicit user correction** — "don't use X", "do it this way", "I told you before". This is **not a requirement change** (those go through modification-guide as a CHG); it corrects "approach/style/taboo" and must be recorded so it isn't repeated.
- **pattern record (KN)**: an **AI-observed recurrence** — the same need/purpose keeps showing up across CHGs/requirements. Recorded **autonomously** as a shallow record, promoted to deep by uncorrected use (see lifecycle below).

Location: `docs/knowledge/` (suggest `errors.md`, `directives.md` — or a combined `knowledge.md` with an INDEX). **Read the index on entry, load only in-scope entries** (see retrieval below and handshake).

## Recording correction directives (req 3)

When you receive a user correction (not a requirement change), **write it into the knowledge base immediately**, not just fix it in the moment:

```markdown
## DIR-<n> — <one-line rule>
- date / branch: YYYY-MM-DD (UTC+0) / <branch>
- context: <when it applies>
- rule: <do / don't>
- reason: <why (user's reason or inferred)>
- source: <summary of the user's instruction>
- confidence: user-confirmed / agent-inferred   ← who established the rule (see priority below)
- status: active
```

## Updating an existing directive (req 4)

When a directive is **updated later**, **rewrite the existing entry, don't add a contradictory new one**:

- Find the matching DIR entry → update the rule; move the old wording to "history" or mark it superseded, keeping dates.
- Goal: each rule always has exactly **one current version**, so the knowledge base doesn't contradict itself (that would be a form of drift).
- If the new directive conflicts with the old, the new wins and record "supersedes DIR-x (reason)".

## Priority and conflict handling (req 5)

The knowledge base is a **high-priority rule set**, not optional advice — it represents "the user already taught this; don't repeat it".

**Confidence & lifecycle (one ladder, pollution-guarded)**: since every later session obeys this file, a wrong or over-generalized entry poisons everything downstream. Every rule sits on one ladder:

| Tier | Who established it | Behavior | Overriding it |
|------|--------------------|----------|---------------|
| **shallow** (KN) | AI observed a recurrence — a **hypothesis** | apply + **announce each use**; every uncorrected use increments `applied` | one plain user sentence |
| **deep** (KN) | shallow that survived use (`applied ≥ 3`, no correction) | apply by default **without per-use announcement**, but listed in the handshake ack | one plain user sentence |
| **user-confirmed** (DIR) | the user said it explicitly (or confirmed a KN) | binding | triple confirmation below |

- **Promotion**: shallow → deep when `applied ≥ 3` with no correction (threshold adjustable; record the promotion date). KN → DIR only via an **actual user statement** — never self-promote.
- **Demotion**: a corrected deep record drops back to shallow or is retired (root cause noted); if the correction states a rule, that becomes a DIR (the reverse got established).
- Agents must never record an entry as user-confirmed without an actual user statement.

## Autonomous triggering (shallow records)

Don't wait to be corrected — **the same need/purpose appearing a second time across CHGs/requirements triggers a shallow record** (threshold 2, adjustable). It may span sessions, so **the evidence and counters live in the entry, not in memory**. Checked at CHG close-out (see modification-guide): does this change's motive repeat a prior CHG's?

```markdown
## KN-<n> — <one-line rule hypothesis>
- tier: shallow / deep(+ promotion date)
- date / branch: YYYY-MM-DD (UTC+0) / <branch or all-branches>
- tags/scope: <module / topic — the retrieval keys>
- evidence: <CHG-… ids / requirement mentions (≥2 occurrences)>
- counters: seen <n> / applied <n> / last-applied <date>
- status: observing / active / retired (reason)
```

## AI-friendly structure & scoped retrieval (INDEX)

Nobody reads the whole knowledge base — that's catalog-thinking. The file **starts with an INDEX**; entries are anchored sections with `tags/scope`:

```markdown
## INDEX (read this, not the whole file)
| id | tier | tags/scope | one-line rule | status |
|----|------|-----------|---------------|--------|
| DIR-1 | user-confirmed | all-branches · api | amounts always integer minor units | active |
| KN-2 | deep | report | exports always UTF-8 BOM | active (applied 5) |
| KN-3 | shallow | payment | prefer dry-run first | observing (seen 2 / applied 1) |
```

Retrieval rule (entry and dispatch alike): read the INDEX → load **global entries + entries whose tags intersect your current scope** — nothing else. Dispatch briefings carry the matching entries the same way (see handshake's scoped tier).

- Read it on entry (handshake); planning and implementation must obey current directives.
- **When the knowledge base conflicts with a new user request** (the new request would violate a directive): **do not decide unilaterally** (neither silently follow knowledge nor silently follow the new request). Use **triple confirmation + impact disclosure**:
  1. **First**: point out the conflict — "this contradicts DIR-x '…'", and **explain the impact** (what it touches, why it was set, the risk).
  2. **Second**: ask the user to explicitly override that rule (not offhand), listing the affected scope again.
  3. **Third**: final confirm "override DIR-x for sure?"; only proceed on a yes.
- All three confirmed → proceed, and **update the knowledge base**: mark that directive "overridden/relaxed by user on <date> (reason)" or rewrite the rule; not silently ignored.
- If any of the three isn't clearly confirmed → keep the directive, don't do the conflicting action.

> Why three: overturning a high-priority rule should be a deliberate, traceable decision, not a one-liner reversal; triple confirmation + impact disclosure lets the user decide fully informed and leaves a record.

## Relation to the rest of the flow

- With agent-worklog: worklog collects "errors"; this file spells out KB governance (directives, updates, priority, conflict); the parent agent consolidates errors and directives here.
- With handshake: the KB is a required read on entry.
- With modification-guide: **requirement change → CHG**; **correction directive → knowledge**. Keep them separate.
- With branch-isolation: tag directives with a branch; cross-branch reference follows the requirement rule (default: current branch only; a general rule may be tagged "all branches").
