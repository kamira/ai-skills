---
name: execution-plan
description: >
  Executable plan format for autopilot runs: a Global Constraints block that binds every task,
  plus per-task Interfaces (consumes/produces) and a test line, tracked with checkboxes. The plan
  lives inside the target project's CHG (modification-guide section) — never in a separate file.
  Read this when writing or validating a plan, before the first task is built.
---

# execution-plan — the plan that a machine can drive

> 語言 / Language: [繁體中文](execution-plan.zh-tw.md) · **English**

## Why this format

A plan drives an autopilot only if every task is **independently executable and independently checkable**: an agent that sees nothing but the Global Constraints + one task entry must be able to build it, and a reviewer that sees nothing but the same brief + the diff must be able to judge it. Prose plans ("then improve the API") fail both tests.

## Format (inside the CHG's modification-guide section)

```markdown
### Global Constraints (every task must obey)
- <testable constraint — "always X", never "prefer X">

### Tasks (checkboxes = resume points)
- [ ] T1. <title>
  - interfaces: consumes <inputs/preconditions> / produces <outputs/deliverables>
  - test: <how to verify — a command or an assertable condition>
- [ ] T2. ...

### Acceptance operation (the end-stage operational test — required for code-bearing changes)
- operate: <how to run/exercise the change for real — a command or steps>
- observe: <what observable behavior confirms it works>
- pass: <pass criteria>
```

For a **pure-doc CHG** with nothing to run, replace the whole section with a one-line header field: `Acceptance-operation: n/a (docs-only)`.

## Rules (plan-check enforces these)

- A **Global Constraints** section must exist. Put version floors, naming rules, exact values here — anything that binds *every* task. Fold in the applicable knowledge globals and Guideline constraints so the task brief is self-contained.
- Every task carries an **`interfaces:` line** (what it consumes and produces — this is what makes tasks composable and reviewable) and a **`test:` line** (command or assertable condition; docs-only tasks state a reproducible check instead).
- Task ids **T1..Tn sequential**; each task sized so one agent run completes it (bite-sized; if a task needs its own plan, it is too big — split it).
- Ticks are written **the moment a task passes review** — they are the resume points after any interruption (crash-only discipline).
- **`### Acceptance operation`** declares the end-stage operational test (`operate`/`observe`/`pass`). This is **not** a per-task `test:` line — task tests are unit/build level, this runs the whole change for real. plan-check only *hints* if it is missing (non-blocking); the **run**-time operational-verify stage enforces it (a code CHG without it, and without a `docs-only` marker, halts before acceptance — see autopilot-loop).

## Relation to the ledger

The plan **is** the CHG's modification steps — one artifact, one truth. plan-check (`autopilot_runner.py plan-check`) is the machine gate; a plan that fails it never starts running (exit 2).
