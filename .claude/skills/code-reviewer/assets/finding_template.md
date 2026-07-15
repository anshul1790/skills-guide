# Finding Format

Use this exact shape for every finding you report, whether you're printing
plain text or filling in a structured findings tool. Consistency here is
what makes a review easy to scan quickly.

```
### [SEVERITY] path/to/file.ext:line — one-line summary of the defect

**Scenario:** the specific input, sequence of calls, or state that
triggers it, and what goes wrong as a result (wrong output, crash, data
exposure). This is the part that proves it's a real bug, not an opinion.

**Fix:** (optional, one line) the direction of the fix, only if it's not
obvious from the scenario.
```

## Rules

- **Order findings most-severe-first**: all Critical findings, then all
  Important, then all Minor. Within a tier, order by file.
- **One finding per concrete issue.** Don't bundle two unrelated problems
  in the same file under one heading — a reader needs to be able to
  address them independently.
- **The summary is not the scenario.** "off-by-one in chunking" is a
  summary; "chunkArray([1,2,3,4], 2) returns [[1],[3]] instead of
  [[1,2],[3,4]], silently dropping every second element" is the scenario.
  Always include both.
- **If you find nothing**, say so directly — "No correctness or security
  issues found; the diff looks safe to merge as-is" — rather than
  inventing Minor findings to avoid an empty report. An honest "nothing to
  flag" is more useful than manufactured nitpicks.

## If a structured findings tool is available

Some environments expose a dedicated tool for reporting review findings
(check your available tools for one that accepts a list of findings with
fields like category/file/line/summary/failure_scenario). When one is
available, use it instead of hand-formatting text — map:

- `summary` → the one-line summary
- `failure_scenario` → the **Scenario** content
- `file` / `line` → the location
- `category` → a short slug: `correctness`, `security`, or
  `maintainability`

Fall back to the plain-text format above only when no such tool exists in
the current environment.
