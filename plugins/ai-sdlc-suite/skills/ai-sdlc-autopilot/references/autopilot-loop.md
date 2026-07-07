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
  → whole-branch review → acceptance (ACC; per policy self-verify / independent)
  → PR → merge (per policy) → close-out: CHG status + Commit/PR + recurrence check + knowledge
```

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
plan-check --chg <CHG.md>                      # validate plan format only
run  --chg <CHG.md> --repo . [--agent-cmd T] [--test-cmd C] [--dry-run] [--no-commit] [--max-tasks N]
status --chg <CHG.md>                          # ticked/unticked, next task, current stage
```

Exit codes: `0` done · `1` unexpected error · `2` invalid plan · `3` legitimate halt (reason printed). Wire cron/CI on 3 (notify a human with the reason) and 0 (pick up the next CHG). `--dry-run` simulates build/test/review success to exercise the state machine and halt policy without an agent.

## Degraded modes

- **No headless agent** (`--agent-cmd` unset, not dry-run): the runner prints each task brief and halts (exit 3) — human-in-the-loop mode; ticks still drive resume.
- **No gh CLI**: PR/merge stages print the exact commands to run and halt (exit 3) instead of merging.
- **No spawn for reviews**: the same agent builds and reviews serially — note the degradation in the ACC (same rule as ai-sdlc's degraded panel).
