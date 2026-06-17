---
name: ci-cd
description: >
  Optional: wire ai-sdlc's document governance into CI/CD so "documents are the truth" is enforced
  by machine, not just by discipline. Opt in per solo or team need — read this when a project has or
  is adopting CI/CD (GitHub Actions / GitLab CI / Jenkins, etc.) and you want acceptance and
  structure-consistency to become PR gates. Covers governance-artifact-to-gate mapping, recommended
  gates, and a platform-neutral example. Projects without a pipeline can skip this.
---

# ci-cd (optional) — wire governance into CI/CD

> 語言 / Language: [繁體中文](ci-cd.zh-tw.md) · **English**

## Purpose (optional)

**Opt in per solo or team need.** If a project has CI/CD, turn ai-sdlc's document governance into **automated gates** so "documents are the truth", "trace every change", and "acceptance aligns to source" are enforced by machine rather than by discipline. **Projects without a pipeline can skip this** and rely on the ai-sdlc flow. Solo projects are often simpler; teams need it more; either may opt in.

## When to read

- A team project has or is adopting CI/CD
- You want acceptance and structure-consistency to become merge / PR gates
- Multi-person / multi-agent collaboration that needs machine enforcement so nobody skips governance

## Governance artifact → gate mapping

| ai-sdlc artifact | CI/CD counterpart |
|------------------|-------------------|
| Acceptance criteria (Guideline §7 / ACC) | automated tests; CI runs them as a gate |
| Change record CHG | required PR template field; PR must link the CHG |
| Structure docs `docs/structure/` | structure-drift check (below) |
| Acceptance report ACC | merge gate: no matching, passing ACC → no merge |

## Recommended gates (loose → strict; pick per team needs)

1. **Tests must be green**: maps to acceptance criteria; the baseline.
2. **PR must link a CHG**: PR description must contain a `CHG-` reference (maps to "trace every change").
3. **Structure-sync check**: if this PR changed structural code (e.g. `src/models/**`, schema) but didn't update `docs/structure/`, warn or block (maps to "documents are the truth").
4. **Acceptance gate**: an ACC for this change exists and concludes "pass" before merge (maps to "close acceptance in the same round").

Adopt **loose → strict**: start with "tests green + PR links CHG", and once the team is used to it add structure-sync and the ACC gate, so you don't stall the flow by being too strict at once.

## Platform-neutral example (pseudo)

Conceptual sketch; translate to any CI platform (GitHub Actions / GitLab CI / Jenkins...):

```yaml
on: pull_request
jobs:
  governance:
    steps:
      - run: <run tests>                    # gate 1: tests green
      - check: PR body contains "CHG-"      # gate 2: traceability
      - check: if changed_files match structural paths (src/models|schema),
               then docs/structure/ must also have changes        # gate 3: structure sync
      - check: docs/acceptance has an ACC for this CHG concluding "pass"  # gate 4: acceptance gate
```

GitHub Actions example: trigger on `on: pull_request`; `gate 1` runs the test step; `gate 2/3/4` use a script that reads the PR body and `git diff --name-only`, compares paths, and greps `docs/acceptance/` for the matching file — any failing check exits non-zero to block the merge. Other platforms (GitLab CI `rules`, Jenkins stages) work the same way.

## Relation to the base flow

CI/CD **does not replace governance; it enforces that governance is followed**. ai-sdlc defines "what documents to produce and how to verify"; this file turns those into machine-checkable gates. The team edition especially needs it — with more people, discipline alone is unreliable. Optional: without a pipeline, rely on the ai-sdlc and cross-agent flows.
