---
name: ai-sdlc-autopilot
description: >
  Governed autopilot execution layer on top of ai-sdlc: turns a confirmed requirement into an
  auto-completed change — plan (Global Constraints + per-task interfaces) → per-task TDD build
  with read-only task review → acceptance → commit → PR → merge — with halt points driven by
  ai-sdlc risk grading (low = full auto, medium = one confirm gate, high / irreversible = always
  halts for a human). Use when the user wants a change executed end-to-end automatically under
  governance, wants TDD / per-task-review discipline, or wants to run the autopilot runner.
  Requires the ai-sdlc skill (>= v1.17) as the governance layer — run its entry handshake first.
metadata:
  version: 1.1.0
---

# ai-sdlc-autopilot — governed autopilot execution

> 語言 / Language: [繁體中文](SKILL.zh-tw.md) · **English**

**One sentence**: ai-sdlc keeps the ledger and the gates; this skill does the building and the driving — a requirement goes in, a governed, reviewed, tested, merged change comes out, and every step lands in the ai-sdlc ledger automatically.

Three layers: **governance** (ai-sdlc, external, read-only), **execution** (the references here: plan format, TDD, task review, debugging), **drive** (autopilot-loop contract + `assets/autopilot_policy.json` + `scripts/autopilot_runner.py`).

## Hard dependency: ai-sdlc is the governance layer

- **Entry handshake first** (ai-sdlc handshake), CHG before building, acceptance in the same round, knowledge close-out — none of this is optional, and none of it is duplicated here.
- This skill **reads ai-sdlc, never modifies it**. Version self-check on entry: ai-sdlc >= v1.17 (recurrence field + knowledge bootstrap are assumed by the close-out automation).
- **No parallel ledger**: the plan lives in the target project's CHG (modification-guide section), review verdicts land in the ACC evidence column, errors land in `docs/knowledge/`. If you find yourself writing to a new docs directory, you are drifting.

## Detect → load

| Situation | Cues | Load |
|-----------|------|------|
| Writing / validating an executable plan | task breakdown, constraints, interfaces, "plan this" | [`references/execution-plan.md`](references/execution-plan.md) |
| Building a task | implement, code it, red-green, test-first | [`references/tdd-loop.md`](references/tdd-loop.md) |
| A task's diff needs judging | review this task, verdict, spec compliance | [`references/task-review.md`](references/task-review.md) |
| Tests keep failing | 2+ consecutive failures on one task | [`references/systematic-debugging.md`](references/systematic-debugging.md) |
| Running the whole flow / resuming / wiring CI | autopilot, run it end-to-end, resume, halt policy | [`references/autopilot-loop.md`](references/autopilot-loop.md) |

## The loop

```
ai-sdlc handshake → CHG (plan-check gate)
  → [ per task: TDD build → unit/build tests → read-only task review → tick + commit ]
  → whole-branch review → operational verify (run it for real) → ACC → PR → (policy) merge → knowledge close-out
```

Interruption at any point is safe: ticked checkboxes are the resume point, and the live handshake file (`docs/worklog/handshake-autopilot.md`) is updated at every task boundary.

**Task tests ≠ acceptance**: per-task `test:` is unit/build level; before ACC the runner requires an **operational test** (the plan's `### Acceptance operation` — operate/observe/pass, run for real). A code CHG without it (and without a `docs-only` marker) halts before acceptance — see autopilot-loop.

## Halt policy (risk × stage — tighten only)

| Risk | confirm gate | task review | operational verify | acceptance | PR | merge |
|------|--------------|-------------|--------------------|------------|----|-------|
| low | auto | auto | auto (verify-cmd / human) | auto (self-verify) | auto | auto |
| medium | **confirm** (pre-authorizable) | auto | auto (verify-cmd / human) | auto | auto | auto |
| high | **halt** | auto | **halt** (human-performed) | **halt** (independent verifier) | auto | **halt** |

**Permanent halts** (never automated, hard-coded, no config can relax them): irreversible deletion, payments, production data migration, security-boundary changes. Decision order: permanent halts → CHG `Autonomy:` field (tighten only) → policy matrix → unknown = halt.

## Runner

```
python3 scripts/autopilot_runner.py plan-check --chg <CHG.md>
python3 scripts/autopilot_runner.py run --chg <CHG.md> --repo . \
    [--agent-cmd 'claude -p "$(cat {brief})"'] [--test-cmd 'pytest -q'] [--verify-cmd './run-smoke.sh'] [--dry-run] [--no-commit]
python3 scripts/autopilot_runner.py status --chg <CHG.md>
```

`--test-cmd` = per-task unit/build tests; `--verify-cmd` = the end-stage operational test (run the change for real). Without `--verify-cmd` the operational-verify stage halts (exit 3) for a human to perform it.

The runner contains **no LLM**: it is a state machine and referee — the building and reviewing are done by whatever headless agent command you configure. Exit codes: `0` done, `1` unexpected error, `2` invalid plan, `3` legitimate halt (the reason is printed; wire cron/CI on these).

## Storage convention

Everything lands in the **target project's** existing ai-sdlc ledger — see the mapping in [`docs/ai-sdlc-autopilot/structure/data.md`](../../docs/ai-sdlc-autopilot/structure/data.md) (plan → CHG, verdicts → ACC evidence, root causes → knowledge, one commit per task carrying the CHG id).

## NOTICE (attribution)

The execution methodology here — the plan's Global Constraints / per-task Interfaces blocks, single-reviewer dual verdict (spec + quality) with a legitimate "cannot-verify from diff" outcome, end-of-run whole-branch review, and the TDD / systematic-debugging discipline — is adapted from **Superpowers** by Jesse Vincent (obra), MIT License, © 2025 Jesse Vincent. See [`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md). Differences: outputs land in the ai-sdlc ledger (no separate plans/specs directories), triggering is skill-detection + runner (no harness hooks), and halts are driven by governance-layer risk grading.
