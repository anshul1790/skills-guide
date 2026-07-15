# Maintainability Checklist

Apply this one lightly — it's real but lower stakes than correctness or
security, and it's easy to let it balloon into nitpicking. Skip anything a
linter or formatter would already catch (spacing, import order, quote
style); focus on things that require actual judgment.

- **Naming**: does a name accurately describe what the thing holds or
  does? Flag names that are actively misleading (a variable called
  `isValid` that actually holds a count), not just names you'd have
  chosen differently.
- **Duplication**: is genuinely identical logic repeated in a way that
  will drift out of sync when one copy is fixed and the other isn't?
  Incidental similarity (two 3-line blocks that happen to look alike but
  serve different purposes) isn't duplication — don't flag it.
- **Dead code**: does the diff introduce a function, branch, or variable
  that's never reached or used?
- **Complexity**: is there a control-flow structure (deep nesting, a long
  conditional chain) that obscures what the code actually does, where a
  straightforward restructure would make the logic obviously correct at a
  glance instead of requiring careful reading?
- **Comments**: is there a non-obvious constraint, workaround, or "why"
  that a future reader would need and can't get from the code itself? Only
  flag a *missing* comment when the code's behavior would otherwise
  surprise someone — don't ask for comments that just restate the code.

Keep findings here to genuinely load-bearing issues. A review that's
mostly maintainability nitpicks buries the correctness and security
findings that actually matter.
