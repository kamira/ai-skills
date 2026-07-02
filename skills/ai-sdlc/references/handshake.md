---
name: handshake
description: >
  Entry handshake protocol: every agent / session / handoff does a "handshake" before acting — read
  existing docs in a fixed order, extract the key points, and echo back its understanding, so it can
  take over safely. Read this when you just entered, are taking over an existing project, or handing
  off across sessions/agents. Defines what to read, the order, the key points, and the entry
  acknowledgement (ack) format. It is the executable form of the Session startup check.
---

# handshake — entry handshake protocol

> 語言 / Language: [繁體中文](handshake.zh-tw.md) · **English**

## Purpose

Any agent, on entry (new session, takeover, handoff), first does a "handshake": **read existing docs in a fixed order → extract key points → echo back understanding**, then start work. The goal is auditable handoff and avoiding the drift/misunderstanding caused by "acting without reading". This is the executable form of the Session startup check.

## What to read (fixed order)

1. **Current branch**: first confirm which branch you're on (see branch-isolation); afterwards only reference that branch's requirements/acceptance.
2. **`docs/ai-guideline.md`**: the current Guideline — goals, scope, current **version**, open items.
3. **`docs/knowledge/`**: known errors and **user correction directives** (see knowledge) — avoid repeats; high priority.
4. **`docs/coordination.md`**: org/claims — your role, locked scope, read/write permission, others' in-progress work.
5. **`docs/changes/` + `docs/acceptance/`**: any unclosed stage (CHG not accepted / missing ACC); close first, then start new.
6. **`docs/structure/`**: current structure, check for drift vs code (see doc-integrity).

## Key points (must capture)

- **Current branch** and its scope (don't reference other branches' requirements).
- **Current Guideline version** and open items.
- **Your role / read-write permission** (role_refs, tools allowlist).
- **Known errors and correction directives** (knowledge, high priority).
- **Unclosed stages** (hanging acceptance).
- **In-progress claims** (avoid collisions).

## Echo acknowledgement (handshake ack — required before acting)

After reading, **echo your understanding in a few lines before acting**:

```
[handshake] branch: <branch> | role: <role> (RW: <scope>)
current Guideline: v<x>; unclosed: <CHG-… pending acceptance / none>
must follow (knowledge): <key entries / none>
next I will: <one line>; halt: <per autonomy, this gate auto/halt>
```

The echo lets a human/parent intercept misunderstanding before you act; across agents it's proof of "I took over correctly".

## Relation to the rest of the flow

- Concretizes the Session startup check; the read list maps to knowledge / branch-isolation / doc-integrity / coordination / autonomy.
- Machine aids: use `scripts/role_loadout.py` for the role's references to load; `scripts/doc_integrity_check.py` to scan for unclosed items and drift.
- If you find unclosed items / drift / conflict → handle it per the matching reference before starting new work.
