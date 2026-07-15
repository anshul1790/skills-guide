# Severity Rubric

Consistent severity labeling matters more than people expect: a reviewer
that calls everything "Critical" trains the reader to ignore the label
entirely, and one that calls real bugs "Minor" gets them shipped. Use these
three levels, and hold the line on what qualifies for each.

## Critical

Will produce wrong behavior, a crash, data loss, or a security exposure on
a **realistic, likely-to-occur path** — not a contrived edge case nobody
will hit. If you can describe a normal user action or common input that
triggers it, it's Critical.

Examples: SQL/command injection from user input, an off-by-one that drops
real data, a null-dereference on a value that's null in the common case,
a missing auth check on a sensitive endpoint, a race condition in code that
runs concurrently by design.

## Important

A genuine bug or risk, but gated behind an edge case, an unlikely input, or
a degraded (not broken) outcome. Worth fixing before merge in most cases,
but the world doesn't end if it ships and gets caught in the next pass.

Examples: an unhandled error path that only triggers on a rare upstream
failure, a resource leak that matters under sustained load but not in
normal usage, inconsistent handling of an edge case (e.g. empty array)
that's unlikely but possible.

## Minor

Real but low-stakes: readability, naming, minor duplication, a comment
that's gone stale, a slightly awkward structure. Nothing here changes
program behavior.

Examples: a variable name that doesn't match its contents, a repeated
3-line block that could be a helper, a magic number that could be a named
constant.

## What does NOT belong in any severity tier

A style or taste preference that isn't backed by a concrete failure
scenario isn't a finding at all — it's an opinion. If you can't describe
a specific input or state that produces a wrong result, don't report it as
a bug; either leave it out or, if it's worth mentioning, frame it clearly
as a suggestion rather than a defect. Padding a review with invented
"Minor" issues to look thorough is worse than a shorter, accurate review —
it trains the reader to skim past your findings.
