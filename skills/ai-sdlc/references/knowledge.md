---
name: knowledge
description: >
  Knowledge base governance: record "errors hit during execution" and "user correction directives"
  so the AI doesn't repeat them; when a directive is updated, overwrite in place (no contradictory
  duplicates); the knowledge base is a high-priority rule set, and when it conflicts with a new user
  request it requires triple confirmation plus impact disclosure. Read this when you receive a
  correction, before entry to avoid repeats, or when a request conflicts with a known rule.
  Distinction: requirement changes go through modification-guide; correction directives go here.
---

# knowledge — error & correction-directive knowledge base

> 語言 / Language: [繁體中文](knowledge.zh-tw.md) · **English**

## Purpose

The knowledge base is the durable memory that keeps the AI from repeating the same mistakes. Two entry types:

- **error**: technical errors hit during execution and their fixes (from agent-worklog).
- **directive**: an **explicit user correction** — "don't use X", "do it this way", "I told you before". This is **not a requirement change** (those go through modification-guide as a CHG); it corrects "approach/style/taboo" and must be recorded so it isn't repeated.

Location: `docs/knowledge/` (suggest `errors.md`, `directives.md`, or a combined `knowledge.md`). **Read on entry** (see handshake).

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

**Source confidence (pollution guard)**: since every later session obeys this file, a wrong or over-generalized entry poisons everything downstream. Tag each entry:
- `user-confirmed` — the user explicitly said it (or confirmed an inference). **Binding**; overriding requires the triple confirmation below.
- `agent-inferred` — an agent generalized it from observation. **Advisory**: follow it by default, but a plain user instruction overrides it (no triple confirmation); the first time it's applied in a session, say so — giving the user the chance to confirm it (upgrade to user-confirmed) or discard it. Agents must not record an entry as user-confirmed without an actual user statement.

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
