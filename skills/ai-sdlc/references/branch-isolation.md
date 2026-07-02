---
name: branch-isolation
description: >
  Branch isolation: when multiple git branches run in parallel, each branch's requirements, change
  records, acceptance, and verification apply only to THAT branch and must not reference
  requirements opened on other branches. Read this when the project has multiple branches, or when
  you work/verify on a branch. Covers branch tagging, using only the current branch's sources, the
  "brought in only at merge" rule, and the distinction from cross-repo.
---

# branch-isolation — branch isolation

> 語言 / Language: [繁體中文](branch-isolation.zh-tw.md) · **English**

## Purpose

With parallel branches, different branches often open different requirements and changes. **When working or verifying on a branch, all requirements/CHG/ACC/verification may reference only that branch's sources, never requirements opened on other branches** — otherwise you'd verify branch A's code against branch B's requirements, causing wrong gating and scope contamination.

> Distinction from `cross-repo`: cross-repo coordinates a contract across multiple repos; branch-isolation is about multiple branches within one repo not referencing each other's requirements. Both can coexist.

## Rules

- **Tag the branch**: the Guideline / CHG / ACC header has a "Branch" field. When referencing requirements or acceptance criteria, take only those on the **same branch as current**.
- **Only current-branch sources**: in detection/acceptance/impact analysis, filter out other branches' CHGs/requirements. Current branch = the one confirmed in the entry handshake.
- **No cross-branch reference**: branch A's acceptance may not use branch B's requirements as the baseline; branch A's CHG may not cite branch B's requirement as its basis.
- **Brought in only at merge**: another branch's requirements/changes enter the current branch only when **merged in**, via the normal flow (modification-guide + acceptance); before the merge they are "out of this branch's scope".
- **Shared baseline**: genuinely cross-branch requirements/rules belong in a shared baseline (e.g. the main branch, or knowledge tagged "all branches"), not laterally referenced from a feature branch.

## When to read

- The project has multiple branches (feature / release / hotfix…)
- You implement or verify on a branch
- You need to judge which branch a requirement/criterion belongs to

## Template field

Add to the Guideline / CHG / ACC header:

```
- Branch: <branch name>   ← the branch this doc belongs to; reference/acceptance use same-branch sources only
```

## Relation to the rest of the flow

- handshake: the first step on entry is to confirm the current branch; all references afterwards are limited to it.
- modification-guide / acceptance-verification: CHG/ACC carry a branch; the acceptance baseline takes only the same branch's Guideline/CHG.
- doc-integrity: can add a "CHG/ACC branch field = current git branch" check (mismatch → flag).
- knowledge: directives default to the current branch; general ones are tagged "all branches".
