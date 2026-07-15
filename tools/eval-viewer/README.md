# eval-viewer

A standalone tool for browsing skill/agent eval results in a web UI — no
Claude session required to view them once they exist. Two plain Python
scripts, zero third-party dependencies (stdlib only), one HTML template.

```
tools/eval-viewer/
├── generate_review.py      the viewer — serves a live page or writes static HTML
├── aggregate_benchmark.py  turns per-run grading.json files into benchmark.json
├── viewer.html             the page template (CSS + JS baked in)
└── README.md                this file
```

## What it expects on disk

Point it at a "workspace" directory shaped like this:

```
<workspace>/
└── eval-<id>-<name>/
    ├── eval_metadata.json       {"eval_id": 0, "prompt": "...", ...}
    ├── with_skill/
    │   ├── outputs/              any files produced — .md, .json, images, .pdf, .xlsx all render inline
    │   ├── grading.json          {"expectations": [{"text","passed","evidence"}], "summary": {...}}
    │   └── run-1/
    │       ├── grading.json      same content, nested here for aggregate_benchmark.py
    │       └── timing.json       {"total_tokens": ..., "total_duration_seconds": ...}
    └── without_skill/            identical shape — this is the baseline to compare against
```

You don't need every piece — `outputs/` alone is enough to browse results.
`grading.json` unlocks the "Formal Grades" section per run. Adding
`run-1/grading.json` + `run-1/timing.json` and running
`aggregate_benchmark.py` unlocks the "Benchmark" tab with pass-rate/time/token
comparisons between `with_skill` and `without_skill`.

## Usage

**1. Aggregate grading data into a benchmark (optional, skip if you only want to browse outputs):**

```bash
python3 tools/eval-viewer/aggregate_benchmark.py <workspace> --skill-name my-skill
# writes <workspace>/benchmark.json and benchmark.md
```

**2. View the results — pick one:**

Live server (auto-refreshes on page reload if you add more results later):

```bash
python3 tools/eval-viewer/generate_review.py <workspace> \
  --skill-name my-skill \
  --benchmark <workspace>/benchmark.json
# serves on http://localhost:3117 (use --port to change)
```

Static file (no running process — hand the HTML file to anyone, or open it directly):

```bash
python3 tools/eval-viewer/generate_review.py <workspace> \
  --skill-name my-skill \
  --benchmark <workspace>/benchmark.json \
  --static report.html
open report.html
```

Comparing against a previous round of testing:

```bash
python3 tools/eval-viewer/generate_review.py <workspace> \
  --previous-workspace <previous-workspace> \
  ...
```

## How it works

- `generate_review.py` walks the workspace, reads every `outputs/` folder it
  finds, embeds file contents directly into a JSON blob (text inline, images/PDF/xlsx
  as base64 data URIs — no separate file requests needed), and substitutes
  that JSON into `viewer.html` in place of an `EMBEDDED_DATA` placeholder.
- In server mode, this HTML is regenerated fresh on every page load, so a
  browser refresh always reflects whatever is currently on disk.
- The "Submit All Reviews" button in the UI POSTs your typed feedback to
  `/api/feedback`, which writes `<workspace>/feedback.json` — read that file
  back to see what feedback was left, keyed by run id.
- `--static` mode skips the server entirely and just writes the finished
  HTML string to a file — open it in any browser, no Python process needed
  after that point.

## Example

The `git-commit` skill's eval results already use this exact layout — see
`.claude/skills/git-commit-workspace/iteration-1/`. To browse them:

```bash
python3 tools/eval-viewer/generate_review.py \
  .claude/skills/git-commit-workspace/iteration-1 \
  --skill-name git-commit \
  --benchmark .claude/skills/git-commit-workspace/iteration-1/benchmark.json
```

``` bash
$ TOOL=/Users/sahilchoudhary/Code/genai-2026/skills-guide/tools/eval-viewer
WS=/Users/sahilchoudhary/Code/genai-2026/skills-guide/.claude/skills/git-commit-workspace/iteration-1

python3 "$TOOL/generate_review.py" "$WS" \
  --skill-name "git-commit" \
  --benchmark "$WS/benchmark.json" \
  --static "$TOOL/test-report.html" 2>&1

ls -la "$TOOL/test-report.html"

  Static viewer written to: /Users/sahilchoudhary/Code/genai-2026/skills-guide/tools/eval-viewer/test-report.html

-rw-r--r--@ 1 sahilchoudhary  staff  75953 Jul 14 11:40 /Users/sahilchoudhary/Code/genai-2026/skills-guide/tools/eval-viewer/test-report.html
```