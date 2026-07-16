# SPA TDD Kickoff Prompt

Use this to start (or resume) an iterative TDD build of a lightweight SPA with `tdd-agent` and `coding-agent`. Paste the filled-in version below as your message, or reference this file and fill in the blanks inline.

## Output style

Caveman-compressed: drop articles, filler, pleasantries, hedging. Fragments OK. Keep code, file paths, commands, and exact error strings verbatim. (Same directive embedded in `.claude/agents/tdd-agent.md` and `.claude/agents/coding-agent.md` — repeated here since prompt files aren't auto-read by either agent; this file only reaches them if you paste its content into the kickoff message.)

## Template

```
Business use case: <one paragraph — who's the user, what are they trying to do, what does success look like>

Build a lightweight SPA for this, iteratively, via TDD:
1. Spawn tdd-agent — write one failing test for the smallest useful next slice of the use case above.
2. Spawn coding-agent — make that test (and only that test) pass, minimal implementation.
3. Repeat: tdd-agent picks the next thinnest slice once the previous one is green.

Keep it lightweight: no framework/build-tool additions beyond what's already in the project, no speculative abstractions, no tools/tests beyond what the current slice needs.
```

## Example filled-in

```
Business use case: A solo freelancer needs to log hours against clients and see a running total per client for the current month, so they know what to invoice. Success = they can add a time entry (client, date, hours, note) and see a per-client monthly total update immediately.

Build a lightweight SPA for this, iteratively, via TDD:
1. Spawn tdd-agent — write one failing test for the smallest useful next slice (e.g. "adding a time entry appends it to the list").
2. Spawn coding-agent — make that test pass, minimal implementation.
3. Repeat for the next slice (e.g. monthly total calculation, then per-client grouping).

Keep it lightweight: no framework/build-tool additions beyond what's already in the project, no speculative abstractions, no tools/tests beyond what the current slice needs.
```
