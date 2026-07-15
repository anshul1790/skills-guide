---
name: git-commit
description: Generates Conventional-Commits-style commit messages (feat, fix, chore, docs, refactor, test, style, perf, ci, build) by analyzing the actual git diff rather than guessing from the request, detects breaking changes and marks them for major version bumps (feat!/fix! + BREAKING CHANGE footer), then stages and commits with that message. Use this skill whenever the user asks to commit changes, wants a commit message written, says "commit this", is preparing a release or version-bump commit, or mentions conventional commits, semantic versioning, feat/fix prefixes, or breaking changes — even if they never say "generate a commit message" explicitly.
compatibility: Requires a git repository and the git CLI.
---

# Git Commit

Write commit messages that describe what actually changed, not what the user
said changed. The diff is the source of truth — the user's phrasing of the
request is a hint, not the spec. A user asking to "add a config option" might
have actually also fixed a bug along the way; the message should reflect the
diff.

## Workflow

### 1. Gather context

Run these before writing anything:

- `git status` — see what's staged, unstaged, and untracked.
- `git diff --staged` — if something is already staged, this is the diff to
  describe. If nothing is staged, use `git diff` (unstaged) instead, and plan
  to stage the relevant files yourself in step 6.
- `git log --oneline -20` — learn this repo's actual convention before
  assuming standard Conventional Commits. Some repos don't use scopes, some
  capitalize the summary, some don't use Conventional Commits at all. Match
  what's already there rather than imposing a format the repo doesn't use.
  Only fall back to the standard format described below if the history is
  sparse, inconsistent, or this is the first commit.

### 2. Classify the change type

Pick the type that describes the dominant, user-visible effect of the diff —
not the type of file touched. Standard Conventional Commits types:

| Type | When |
|---|---|
| `feat` | Adds new capability or behavior a consumer can observe |
| `fix` | Corrects incorrect behavior |
| `refactor` | Restructures code with no behavior change |
| `docs` | Documentation only |
| `test` | Tests only |
| `style` | Formatting/whitespace, no logic change |
| `perf` | Performance improvement, no behavior change |
| `chore` | Tooling, deps, config, maintenance — no source behavior change |
| `ci` | CI/CD pipeline changes |
| `build` | Build system or packaging changes |

If the diff clearly does two *unrelated* things (e.g. bumps an unrelated
dependency and also adds a new feature), don't force them into one type —
tell the user the diff looks like it covers more than one concern and ask
whether to split it into separate commits before proceeding. If the changes
are related even though they touch multiple types (e.g. a fix that also
updates a doc comment explaining the fix), pick the dominant type for the
header and mention the secondary change as a body bullet instead of forcing
a split.

### 3. Detect breaking changes

Don't wait for the user to say "this is breaking" — scan the diff for
signals yourself:

- A removed, renamed, or resignature'd exported function/class/type/API
- A removed or renamed config key, env var, or CLI flag
- A changed default value that alters existing behavior
- A major-version bump of a dependency that the codebase's public surface
  depends on
- A changed database schema/migration that isn't backward compatible

If you spot one, confirm with the user that it's intentional before marking
the commit as breaking — being wrong in either direction is costly (a missed
breaking change ships silently; a false positive forces an unwanted major
version bump). Once confirmed, mark it two ways per the Conventional Commits
spec so tooling (e.g. semantic-release) picks it up reliably:

- Append `!` right after the type/scope in the header: `feat(auth)!: ...`
- Add a footer: `BREAKING CHANGE: <what breaks and how to migrate>`

### 4. Infer scope

Derive `(scope)` from the changed files — usually the shared top-level
directory or module name (e.g. changes under `src/auth/` → `auth`). Leave
the scope off entirely when:

- The repo's own history doesn't use scopes (check step 1)
- The diff spans multiple unrelated areas with no single natural scope

Don't force a scope just to fill the template — an absent scope is more
honest than a misleading one.

### 5. Write the message

Format: `<type>[(scope)][!]: <summary>`

- Summary: imperative mood ("add", not "added"/"adds"), no trailing period,
  short enough to read as a one-line git log entry (~50-72 chars as a
  guideline, not a hard cutoff).
- Body (optional, add when the diff isn't self-explanatory from the summary
  alone): blank line, then bullet points covering the notable changes and
  *why* if the reason isn't obvious from the diff itself.
- Footer (only when relevant): `BREAKING CHANGE: ...` per step 3, or issue
  references if the user mentions one.

**Example — feat:**
```
feat(auth): add JWT-based session refresh

- Refresh tokens now rotate on each use instead of staying static
- Old refresh tokens are invalidated server-side after rotation
```

**Example — fix:**
```
fix(parser): handle empty input without throwing

Previously an empty string caused an unhandled TypeError instead of
returning an empty result set.
```

**Example — breaking change:**
```
feat(api)!: require pagination params on list endpoints

BREAKING CHANGE: `GET /items` no longer returns the full list by
default. Callers must pass `page` and `limit`, or the request now
returns a 400.
```

**Example — blended (fix with a related doc update):**
```
fix(config): fall back to default timeout when unset

- Fixes a crash when TIMEOUT_MS was left unset in .env
- Updated the config docs comment to note the default
```

### 6. Stage and commit

Once the message is settled:

- Stage only the files relevant to this change — use `git add <specific
  files>`, not `git add -A`/`git add .`, so unrelated in-progress work in
  the working tree isn't swept into the commit.
- Show the user the final commit message before committing.
- Commit with the message via a heredoc so multi-line bodies/footers are
  preserved exactly, e.g.:
  ```bash
  git commit -m "$(cat <<'EOF'
  feat(auth): add JWT-based session refresh

  - Refresh tokens now rotate on each use instead of staying static
  - Old refresh tokens are invalidated server-side after rotation
  EOF
  )"
  ```
- Never run `git push` as part of this skill — that's a separate action the
  user needs to ask for explicitly.
- If there's nothing staged and nothing changed in the working tree, say so
  instead of inventing a commit.
