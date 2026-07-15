---
name: autopilot-loop
description: >
  The drive contract: the state machine from requirement to merge, the halt decision order
  (permanent halts → CHG Autonomy → policy matrix → unknown = halt), resume semantics, ledger
  mapping, and the runner's commands and exit codes. Read this when running the whole flow,
  resuming an interrupted run, or wiring the runner into cron/CI.
---

# autopilot-loop — the drive contract

> 語言 / Language: [繁體中文](autopilot-loop.zh-tw.md) · **English**

## State machine

```
ai-sdlc entry handshake (governance layer — mandatory, includes knowledge INDEX + pending CHG scan)
  → CHG exists & confirmed?  no → requirement/modification governance first (ai-sdlc)
  → plan-check gate (exit 2 on failure — a bad plan never starts)
  → confirm gate            (per policy: auto / confirm / halt)
  → [ per unticked task T_i:
        TDD build → task tests → read-only task review
        → pass: tick + commit "CHG-<id>: T<i> <title>" + update live handshake
        → fail: one fix pass → re-review → second fail = halt ]
  → whole-branch review
  → operational verify (run it for real: operate → observe → pass; per policy)
  → acceptance (ACC; per policy self-verify / independent)
  → PR → merge (per policy) → close-out: CHG status + Commit/PR + recurrence check + knowledge
```

## Operational verify — the last mile (task tests are not enough)

Per-task `test:` lines are **unit/build level** (RED-GREEN — the parts are correct). They do **not** prove the change actually runs and was actually exercised — the classic "all green, feature still broken" blind spot. Before acceptance the runner requires an **operational test**: run the app/change for real, operate it, observe the behavior.

- The plan declares the operational test in a **`### Acceptance operation`** section (`operate:` how to run/exercise / `observe:` what confirms it works / `pass:` pass criteria) — see execution-plan.
- Runner behavior at this stage:
  - `--verify-cmd C` given and stage is `auto` (low/medium): runs `C`; non-zero → halt (exit 3, "operational verify failed").
  - No `--verify-cmd` (and not dry-run): prints the `### Acceptance operation` brief and halts (exit 3) — **human-in-the-loop**: perform the operation, record evidence in the ACC, then continue to merge.
  - Stage is `halt` (high risk): **always human-performed** — a high-risk operational sign-off is not machine-self-certified, even with a passing `--verify-cmd`.
  - `--dry-run`: simulates operate/observe/pass.
- **Docs-only exemption**: a CHG that declares `Acceptance-operation: n/a (docs-only)` (and has no `### Acceptance operation`) skips this stage — no faked operation for pure-doc changes.
- **A code-bearing CHG with neither `### Acceptance operation` nor a docs-only marker halts here (exit 3)** — you cannot reach ACC on a code change without an operational test on record.

## Halt decision order (strict, tighten-only)

1. **Permanent halts** — task or CHG tagged `permanent-halt:<class>` (irreversible-delete / payments / prod-migration / security-boundary): unconditional halt; the runner refuses any config that relaxes these.
2. **CHG `Autonomy:` field** — may only tighten relative to policy.
3. **`assets/autopilot_policy.json`** — the risk × stage matrix.
4. **Unknown → halt.** A gate the contract doesn't recognize stops the run; guessing "auto" is how autopilots crash.

`confirm` stages may be pre-authorized via a knowledge directive (narrow class, auto-revoked on misfire) — ai-sdlc's pre-authorization rule, unchanged.

## Resume semantics

Ticked checkboxes = completed tasks; rerunning `run` skips them and continues from the first unticked task. The live handshake file (`docs/worklog/handshake-autopilot.md`) is rewritten at every task boundary — an interruption at any moment leaves it current. Working-tree reconciliation on re-entry belongs to the ai-sdlc handshake, not to the runner.

## Runner commands & exit codes

```
plan-check --chg <CHG.md>                      # validate plan format only (operational-test hint is non-blocking)
run  --chg <CHG.md> --repo . [--agent-cmd T] [--test-cmd C] [--verify-cmd V] [--dry-run] [--no-commit] [--max-tasks N]
status --chg <CHG.md>                          # ticked/unticked, next task, current stage
```

`--test-cmd` runs each task's unit/build tests; `--verify-cmd` runs the end-stage operational test (operate the change for real). Exit codes: `0` done · `1` unexpected error · `2` invalid plan · `3` legitimate halt (reason printed). Wire cron/CI on 3 (notify a human with the reason) and 0 (pick up the next CHG). `--dry-run` simulates build/test/review **and operational verify** success to exercise the state machine and halt policy without an agent.

## Degraded modes

- **No headless agent** (`--agent-cmd` unset, not dry-run): the runner prints each task brief and halts (exit 3) — human-in-the-loop mode; ticks still drive resume.
- **No `--verify-cmd`** (and not dry-run): the runner prints the `### Acceptance operation` brief and halts (exit 3) — human performs the operational test and records evidence in the ACC.
- **No gh CLI**: PR/merge stages print the exact commands to run and halt (exit 3) instead of merging.
- **No spawn for reviews**: the same agent builds and reviews serially — note the degradation in the ACC (same rule as ai-sdlc's degraded panel).
