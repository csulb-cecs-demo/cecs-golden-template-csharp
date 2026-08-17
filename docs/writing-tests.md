# Writing tests with the CLI

How to express "is this submission correct?" as a declarative `tests` block
with `gh teacher`.

Assumes you've been through [Getting started with the CLI](getting-started.md).

> [!TIP]
> Prefer the browser? Use
> [Writing tests with the Web UI](writing-tests-web.md).

---

## The three test types

Every test is one of three shapes. Pick by *what you are checking*, not by what
language the assignment is in.

| Type | Checks | Reach for it when |
|---|---|---|
| `run` | A command's **exit code** | Does it compile? Does it import? Does it exit 0? |
| `io` | A command's **stdout** against expected text | Program reads input, prints output |
| `python` | A **pytest suite**, points split per case | You have real unit tests |

### `run` — does the command succeed?

The simplest and most underrated. Exit code 0 passes.

```sh
gh teacher assignment test add <org> <classroom> <slug> \
    --name "compiles" --type run \
    --run "gcc -o hello hello.c" --points 1
```

Require a *specific* exit code with `--exit-code`:

```sh
    --name "exits 42" --type run \
    --run "./prog --selftest" --exit-code 42 --points 1
```

**Lead with a cheap `run` test**: "it compiles," "it imports." When a student
breaks the build, that test names the actual problem instead of letting twelve
downstream tests fail with noise.

### `io` — does it print the right thing?

For programs that read stdin and print stdout.

```sh
gh teacher assignment test add <org> <classroom> <slug> \
    --name "greets Alice" --type io \
    --run "python3 greet.py" \
    --input "Alice" \
    --expected "hello, Alice!" \
    --comparison included --points 2
```

`--comparison` is **required** for `io` and is the whole game:

| Comparison | Passes when | Use for |
|---|---|---|
| `included` | Expected appears **somewhere** in stdout | **Start here.** Tolerates prompts and extra newlines. |
| `exact` | Output matches **exactly** | Output format is itself being assessed |
| `regex` | Expected (a regex) matches stdout | Flexible whitespace, varying numbers |

> [!TIP]
> **Choose `included` unless you mean to grade formatting.** `exact` fails a
> correct program that printed `Enter a name: ` first, and students cannot tell
> a logic error from a trailing-space error. If you *are* grading output format,
> say so in the assignment text. Otherwise it reads as a gotcha.

For long fixtures, use files bundled next to the tests instead of inline
strings: `--input-file names.txt --expected-file expected.txt`.

### `python` — run a pytest suite

```sh
gh teacher assignment test add <org> <classroom> <slug> \
    --name "pytest suite" --type python \
    --setup "python3 -m pip install --quiet -r requirements.txt" \
    --run "python3 -m pytest -q tests/test_stats.py" \
    --timeout 120 --points 12
```

The runner installs `pytest` and `pytest-json-report` if missing, then **splits
the points across the reported cases**. 9 of 12 passing scores 9.

---

## Weighting is by case count

This surprises people, so state it plainly:

> [!IMPORTANT]
> A `python` test carries **one** point value for the **whole suite**. The
> runner divides it across however many cases pytest reports.

So four tests on `mean` and one on `mode` makes `mean` worth **four times** as
much, not because you weighted it but because you wrote more tests. Count
deliberately.

**Corollary: split your assertions.** Each case is one line of feedback. A test
asserting five things reports as one failure and hides the other four, so a
student who fixed three sees no movement. Split them and the score becomes a
gradient instead of a cliff.

---

## Fields at a glance

| Flag | Applies to | Notes |
|---|---|---|
| `--name` | all | Unique within the assignment. Shown to students, so write it as feedback: "handles empty input", not "test 3". |
| `--type` | all | `run` \| `io` \| `python` |
| `--run` | all | The command |
| `--setup` | all | Runs first: compile, install deps. A failure here fails the test. |
| `--points` | all | Defaults to 0 = informational, runs but doesn't score |
| `--timeout` | all | Seconds, 1–600. Default 10. Raise for anything installing packages. |
| `--exit-code` | `run` | Required exit code |
| `--input` / `--input-file` | `io` | stdin, inline or fixture |
| `--expected` / `--expected-file` | `io` | Expected stdout |
| `--comparison` | `io` | **Required.** `included` \| `exact` \| `regex` |

Managing them:

```sh
gh teacher assignment test list <org> <classroom> <slug>          # names
gh teacher assignment test list <org> <classroom> <slug> --json   # full specs
gh teacher assignment test remove <org> <classroom> <slug> <name>
```

### Setting the whole block at once

Adding tests one at a time is fine for two or three. For a suite you keep under
version control, `--tests` takes a JSON file (or `-` for stdin) holding a bare
array of specs and sets the block in one shot:

```sh
gh teacher assignment add <org> <classroom> <slug> --name "..." --tests tests.json
gh teacher assignment test list <org> <classroom> <slug> --json > tests.json   # round-trips
```

Handy when you want the test definitions reviewed in a pull request rather than
typed at a terminal. Mutually exclusive with a per-assignment `autograder.py`.

---

## A worked set

The suite behind this template. A cheap import guard plus the real suite:

```sh
gh teacher assignment test add Giacalone-CECS cecs-378-fa26 lab-01-stats \
    --name "module imports" --type run \
    --run 'python3 -c "import src.stats"' --points 1

gh teacher assignment test add Giacalone-CECS cecs-378-fa26 lab-01-stats \
    --name "pytest suite" --type python \
    --setup "python3 -m pip install --quiet -r requirements.txt" \
    --run "python3 -m pytest -q tests/test_stats.py" \
    --timeout 120 --points 12
```

13 points. A student who breaks the import loses 1 and is told exactly that; a
student whose logic is wrong loses proportionally across the 12.

---

## Traps

**A broken import scores all-or-nothing.** If pytest can't collect, it reports
zero cases and the runner falls back to exit-code scoring. The whole 12 points
vanish together. The 1-point import test is what turns this from a mystery into
a labeled failure.

**Points default to 0.** Omit `--points` and the test runs, reports, and scores
nothing. Occasionally what you want; usually not.

**The default timeout is 10 seconds.** Anything doing `pip install` needs more.
A timeout reads to students as a wrong answer.

**Each submission starts in a fresh grading environment.** Files and installed
packages persist between commands in that submission; shell state does not.
There are no network guarantees beyond package installs, and no clock or
randomness without a fixed seed. A flaky test is a grade appeal.

> [!CAUTION]
> **Never put secrets in a test command.** These run inside the student's repo,
> and a student can print anything the job can read.

---

## When declarative tests aren't enough

Reach for a hand-written autograder when you need partial credit inside a single
test, to inspect files rather than run them, or to hide the tests entirely.

Drop an `autograder.py` at `<classroom>/autograders/<slug>/` in your
organization's `classroom50` config repo. It takes precedence over the `tests`
block for that assignment. A classroom-wide default goes in via
`gh teacher autograder set-default`.

See the [Autograders wiki](https://github.com/foundation50/classroom50/wiki/Autograders).

**Hidden tests, specifically:** don't add secret cases to the suite in the
template, because students receive that repo. Put them in `autograder.py` in the
config repo, which is never distributed. Weigh the cost: hidden tests move
failures from "I can reproduce this locally" to "I have to guess," which is a
real teaching decision, not just a technical one.

---

## Portable specs — letting the tests live in the student repo

By default the grading spec lives in your `classroom50` config repo and nowhere
else. Students receive the template, but not the thing that scores it. That is
deliberate, and `runner.py` says why in one line:

> The specs are DATA, never code: `run`/`setup` strings are teacher-authored
> shell ... and students can't edit `assignments.json`.

**The misconception worth naming:** that a `tests` block committed to the
template will be used. It won't. C50 reads the spec from the config repo, so a
CI file in the assignment repo is decoration as far as the gradebook is
concerned. This surprises anyone arriving from GitHub Classroom, where
`.github/classroom/autograding.json` shipped inside the student repo.

The cost of the default is portability. An assignment repo is not
self-contained: you cannot hand it to a colleague, run it outside the
classroom, or lift it into another org without re-authoring the spec through
the UI or CLI.

If that tradeoff is wrong for your course, you can invert it.

### How to turn it on

Install the portable autograder at
`<classroom>/autograders/<slug>/autograder.py` in your config repo, then rename
this template's `.classroom50/tests.json.example` to `.classroom50/tests.json`.
The file ships inert on purpose, so renaming it is the opt-in.

It runs in one of three modes, set at the top of the autograder:

| Mode | Behavior |
|---|---|
| `off` | Never reads the student spec. Stock C50. |
| `fallback` | Student spec is used *only* where the classroom has none. **Default.** |
| `prefer` | Student spec wins whenever it is present. |

`fallback` is the default because it is the only mode that cannot change a
grade you already configured. It fills gaps; it never overrides.

### What you are giving up

> [!CAUTION]
> **In `prefer` mode, a student can edit the file that grades them.** Anyone
> who can push to the assignment repo can rewrite the point values, delete the
> failing case, or replace the command with `true`.

Be precise about which part of that is new, because the scary-sounding half
isn't the real one:

| | |
|---|---|
| **Not new** | Arbitrary code execution in CI. The student's code already runs, because that is what grading *is*. |
| **New** | The student controls which commands run and what score comes back. |
| **Blast radius** | Their own submission. The workflow token is scoped to their own repo. |

So this is score forgery, not lateral movement. A student can award themselves
full marks. They cannot reach another student's repo, your config repo, or your
service token.

> [!WARNING]
> Do not enable `prefer` on anything that counts toward a grade unless you
> intend to verify the results by hand. `fallback` on ungraded practice work is
> a much easier thing to defend.

### How you catch it

Prevention isn't available here, so the autograder does attribution instead.
Every result records where its spec came from:

```json
{
  "score": 5,
  "max-score": 10,
  "tests_source": "student-repo",
  "trusted": false,
  "tests_origin": ".classroom50/tests.json"
}
```

Those fields survive collection and land in `scores.json`, so a self-graded
submission is queryable in the gradebook rather than buried in a CI log nobody
opens three weeks later:

```
18:12:22   13/13  source=(absent)      trusted=(absent)
18:55:41    5/10  source=student-repo  trusted=false   <-- untrusted
```

> [!NOTE]
> Results graded the stock way carry no `trusted` field at all, which is why
> the older rows read `(absent)`. Filter on `trusted != false`, not
> `trusted == true`, or you will drop every normally-graded submission.

Two more levers if you want them. `UNTRUSTED_MAX` caps what a self-graded
submission can score, which turns a 100-point self-grant into whatever ceiling
you set. And `PORTABLE_PATHS` controls which filenames count, so you can accept
a GitHub Classroom layout during a migration and drop it afterward.

### What it refuses

The loader treats a student spec as hostile, because it is:

- A symlink pointing outside the checkout is refused, not followed.
- A malformed spec is reported as an **error**, never scored as a zero. A zero
  is a claim about the student's work; a broken config is a claim about yours,
  and conflating them buries the bug.
- Duplicate test names are rejected. Names are row identities in the result,
  so duplicates make the gradebook ambiguous about which row a score belongs to.
- A spec with the wrong `schema` is rejected by name, which is what a
  GitHub Classroom `autograding.json` will hit if you rename it without
  converting it.
---

## Protected files, and what C50 does not have

GitHub Classroom could mark files unmodifiable and tell you when a student
edited one. **Classroom 50 has no equivalent.** The field that looks like it,
`allowed_files`, does something close to the opposite.

`allowed_files` is an *allowlist* of paths that belong to the submission,
written as ordered `.gitignore`-style patterns:

```sh
gh teacher assignment add <org> <classroom> <slug> \
    --allowed-files '*' --allowed-files '!hello.py'   # only hello.py counts
```

On a violation it **deletes the file before grading**. It does not report
anything. Its own schema is explicit about the ceiling:

> ... fails open on git/resource failure, so it is a grading-scope/hygiene
> tool, not a secret-hiding boundary.

**The misconception worth naming:** that `allowed_files` protects your test
suite. It does not. It keeps stray files out of the grading scope, and it will
never tell you a student rewrote `tests/`.

### Detecting edits yourself

The piece you need already exists. The accept commit creates
`.classroom50.yaml`, so the commit that *added* that file is the student's
baseline, and everything between it and `HEAD` is their own work. C50 resolves
the baseline this way itself, keyed on the file rather than the commit subject,
because a subject match is spoofable by reusing the wording.

The portable autograder shipped with this template does the rest. Set the paths
you care about:

```python
PROTECTED_PATHS: tuple[str, ...] = ("tests/**", "requirements.txt")
PROTECTED_POLICY = "report"   # or "zero"
```

Patterns accept `dir/`, `dir/**`, globs, and exact paths. A violation is
recorded in the result and reaches the gradebook alongside the score:

```json
{
  "score": 13,
  "max-score": 13,
  "protected_ok": false,
  "protected_baseline": "42a12474a48c...",
  "protected_violations": ["tests/test_stats.py"],
  "protected_policy": "report"
}
```

That example is the case the feature exists for: **full marks, and the reason
for full marks is the thing you needed to know about.**

`report` is the default on purpose. An edited test file is sometimes a student
debugging rather than a student cheating, and that is a judgment you should make
with the evidence in front of you. Use `zero` only when your syllabus says so.

> [!NOTE]
> `protected_ok` is **absent** when the check did not run, which is deliberately
> different from ran-and-found-nothing. Clean and never-checked are not the same
> claim, so filter accordingly.

### What it cannot do

> [!WARNING]
> This is **detection, not prevention**, the same as GitHub Classroom's was.
> Two specific gaps, worth knowing now rather than discovering later:
>
> - A student can edit a protected file and revert it in a later commit. A
>   `baseline..HEAD` diff will not show it.
> - The baseline itself is only pinned by the ruleset that blocks force-pushes
>   to the default branch. `runner.py` says so directly: on a plan that rejects
>   org rulesets, "that protection silently doesn't apply," making this "a
>   robustness win over subject-matching, not a guarantee."

Everything fails open. No baseline, no git, or any git error skips the check
rather than recording a violation. That asymmetry is deliberate: the
consequence of a false positive lands on a student, so uncertainty must never
read as guilt.
---

## Before you hand it to students

> [!CAUTION]
> Whatever you wrote, **push a deliberately wrong submission and confirm it
> comes back red.** A green run is exactly what an assignment with no tests at
> all produces.
> See [Getting started with the CLI, step 7](getting-started.md#step-7--prove-it-actually-grades).
