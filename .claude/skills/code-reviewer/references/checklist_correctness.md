# Correctness Checklist

Always apply this checklist — it's the core of what a review is for. The
goal isn't to pattern-match against this list; it's to actually trace a
concrete input through the changed code and see whether it produces the
right output. The list below just tells you where bugs tend to hide.

- **Boundary conditions**: loop bounds, array slicing, pagination math,
  `<` vs `<=`. Pick a real value (first element, last element, empty
  collection, single-element collection) and trace it through by hand.
- **Null / undefined / None handling**: does every path that can receive
  an absent value actually check for it before using it? Don't just check
  the happy path the diff was written for — check what callers actually
  pass.
- **Error handling**: are exceptions/rejections caught where they need to
  be, and are they handled correctly (not just silently swallowed)? A
  `catch` block that logs and continues can be just as buggy as no
  `catch` at all if the caller now proceeds with bad state.
- **Concurrency**: if this code can run concurrently (web handlers, async
  tasks, workers), is shared state read-modify-written atomically? A
  "check then act" pattern split across two statements is a classic race.
- **Type mismatches**: implicit coercion bugs (string vs number
  comparison, truthy/falsy surprises), especially in loosely-typed
  languages.
- **Resource handling**: are files, connections, locks, and subscriptions
  reliably closed/released, including on the error path, not just the
  success path?
- **State mutation**: does the diff mutate an object that's shared,
  cached, or passed by reference, in a way that surprises other holders of
  that reference?
- **Operator/logic errors**: `&&` where `||` was meant (or vice versa),
  a comparison direction that's backwards, a negation that's missing or
  extra.

When you find something, don't stop at "this looks wrong" — write down the
actual input or sequence of calls that demonstrates it, the same way
you'd describe a bug report. If you can't construct that scenario, you
haven't confirmed a bug yet.
