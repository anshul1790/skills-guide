---
name: code-reviewer
description: Reviews a local git diff (staged changes, unstaged changes, or against a base branch) for correctness bugs, security issues, and maintainability problems, sizing up the change first and applying severity-calibrated checklists before reporting findings ranked by severity with a concrete failure scenario for each. Use this skill whenever the user asks to review code, review a diff or PR locally, sanity-check changes before committing or pushing, look for bugs, check if something is safe to merge, or wants feedback on work they just wrote — even if they don't say "code review" explicitly, e.g. "can you look over what I changed", "does this look right before I push", "any issues with this function I just added".
compatibility: Requires a git repository, the git CLI, and python3.
---

# Code Reviewer

Review real, traced-through behavior — not vibes. Every finding you report
needs a concrete input or state that produces a wrong result; if you can't
construct that scenario, it isn't a finding yet, it's a hunch. This skill
exists to keep reviews honest in both directions: catching real bugs
without padding the report with invented nitpicks to look thorough.

## Workflow

### 1. Gather the diff

Figure out what to review, in this order of preference:

- If the user names a base branch or PR, use `git diff <base>...HEAD`.
- Otherwise, prefer `git diff --staged` if there's staged content.
- Otherwise, `git diff` (unstaged working tree changes).
- If there's nothing staged or unstaged, review the most recent commit:
  `git diff HEAD~1`.

Only ask the user to clarify scope if genuinely ambiguous (e.g. both
staged and unstaged changes exist and they might mean either). Also run
`git status` so you know the full set of touched files, including new
untracked files that a plain `git diff` won't show — read those directly
with the file-reading tool.

### 2. Size up the change before reading it line by line

Pipe the diff's numstat into the bundled script:

```bash
git diff --staged --numstat | python3 <skill-path>/scripts/diff_stats.py
```

(swap `--staged` for whatever scope you settled on in step 1). This tells
you file count, line churn, and flags when the diff is large enough that a
normal line-by-line pass isn't the right approach. If it flags the diff as
large, say so up front and either focus on the highest-risk files first or
suggest the user split the diff — don't silently skim a 2000-line diff and
present it as a complete review.

### 3. Decide which checklists apply

Read `references/severity_rubric.md` once — it defines what separates
Critical from Important from Minor, and you need that calibration before
you label anything.

Then, per file:

- **Always** apply `references/checklist_correctness.md`.
- Apply `references/checklist_security.md` only when the file actually
  touches user input, auth, queries, file paths, secrets, deserialization,
  or outbound network calls. Don't force a security pass on files that
  have no relevant surface — that just trains the reader to skim past your
  security findings on the files where it matters.
- Apply `references/checklist_maintainability.md` lightly, on every file,
  but keep it secondary to the other two.

### 4. Actually trace the logic — don't pattern-match

For each changed file, read enough surrounding context to judge it
correctly — the diff hunk alone is often not enough, since a bug frequently
depends on how a function is called elsewhere or what state existed before
the change. Pick concrete inputs (first element, last element, empty
input, the value a real caller would pass) and trace them through the
changed code by hand. This is the actual review; the checklists just tell
you where to look.

### 5. Report findings

Format per `assets/finding_template.md` — read it for the exact shape and
ordering rules. In short: most severe first, one concrete issue per
finding, each with a real failure scenario, and if a structured
findings-reporting tool is available in your current environment, use it
instead of hand-formatting text (the asset file explains how to map
fields).

If you find nothing worth flagging, say so plainly. A short, honest
"no significant issues, safe to proceed" is a better outcome than padding
the report with manufactured Minor findings — and it's just as valid a
result of a real review.

### What this skill does not do

It reviews and reports — it does not edit files or commit anything on its
own. If the user wants a finding fixed, that's a separate, explicit next
step (and a good moment to reach for the `git-commit` skill once the fix
is made). It also doesn't post comments to a GitHub PR; it's scoped to
local diffs.
