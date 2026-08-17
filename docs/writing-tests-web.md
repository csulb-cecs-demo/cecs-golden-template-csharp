# Writing tests with the Web UI

How to express "is this submission correct?" with Classroom 50's declarative
autograding form.

Assumes you've been through
[Getting started with the Web UI](getting-started-web.md).

> [!TIP]
> Prefer the terminal, JSON files, or bulk editing? Use
> [Writing tests with the CLI](writing-tests.md). The grading model is the same;
> only the authoring workflow changes.

---

## Open the test editor

For a new assignment, tests appear in the assignment form after you set
**Grading** to **Autograded** and select **Use the built-in autograder**.

For an existing assignment:

1. Open [classroom50.org](https://classroom50.org/), then your organization,
   classroom, and assignment.
2. Click **Assignment settings**.
3. Open **Grading and submissions**.
4. Under **Autograding tests**, click **Add test**.

Test-definition changes are published through the `classroom50` config repo
and apply to existing student repositories on their next graded submission.
This is different from changing the repository template or turning the
built-in autograder on: those provisioning changes affect repositories
accepted from then on, not repositories that already exist.

---

## The three test types

Every test is one of three shapes. Pick by *what you are checking*, not by what
language the assignment is in.

| Web UI type | Checks | Reach for it when |
|---|---|---|
| **Run command** | A command's **exit code** | Does it compile? Does it import? Does it exit 0? |
| **Input/Output** | A command's **stdout** against expected text | Program reads input, prints output |
| **Python (pytest)** | A **pytest suite**, points split per case | You have real unit tests |

There are **no other language-specific test types**. Non-Python languages have to rely on *Run command* and *Input/Output* tests.


### Run command — does the command succeed?

These simple tests run a shell command, and only pass if the command exits with code 0.
Click **Add test → Run command**, then enter:

| Field | Value |
|---|---|
| **Test name** | `Compiles` |
| **Run command** | `gcc -o hello hello.c` |
| **Required exit code** | `0` |
| **Timeout (seconds)** | `10` |
| **Points** | `1` |

To require a specific nonzero exit code, change **Required exit code**. For
example, test `./prog --selftest` with required exit code `42`.

**Recommendation: the first test chould be a cheap Run command test**: something like "It compiles," "It imports," etc. When a student breaks the build, that test names the actual problem instead of letting twelve downstream tests fail with confusing error messages.

### Input/Output — does it print the right thing?

For programs that read stdin and print stdout, click **Add test → Input/Output** and enter:

| Field | Value |
|---|---|
| **Test name** | `Greets Alice` |
| **Run command** | `python3 greet.py` |
| **Input (stdin)** | `Alice` |
| **Expected output** | `hello, Alice!` |
| **Comparison** | **Included** or **Exact** or **Regex** |
| **Points** | `2` |

**Comparison** determines the method for matching stdout to expected otuput:

| Comparison | Passes when | Use for |
|---|---|---|
| **Included** | Expected appears **somewhere** in stdout | **Start here.** Tolerates prompts and extra newlines. |
| **Exact** | Output matches **exactly** after outer whitespace is trimmed | Output format is itself being assessed |
| **Regex** | Expected, treated as a regular expression, matches stdout | Flexible whitespace, varying numbers |

> [!TIP]
> **Choose Included unless you mean to grade formatting.** Exact fails a
> correct program that printed `Enter a name: ` first, and students cannot tell
> a logic error from a formatting error. If you *are* grading output format,
> say so in the assignment text. Otherwise it reads as a gotcha.

The Web UI's Input/Output fields are inline text. For a large fixture, keep the
data and a small comparison script in the template, then use a **Run command**
test to invoke that script. The CLI guide also documents file-backed input and
expected-output fields.

### Python (pytest) — run a pytest suite

Click **Add test → Python (pytest)** and enter:

| Field | Value |
|---|---|
| **Test name** | `pytest suite` |
| **Setup command** | `python3 -m pip install --quiet -r requirements.txt` |
| **Run command** | `python3 -m pytest -q tests/test_stats.py` |
| **Timeout (seconds)** | `120` |
| **Points** | `12` |

The runner installs `pytest` and `pytest-json-report` if they are missing, then
**splits the points across the reported cases**. Nine of twelve passing scores
9.

If several tests need the same dependency installation, put it in the
assignment-level **Setup command** under **Advanced settings** instead of
repeating it on every test.

---

## Setup commands and dependencies

There are two places to run setup:

| Location | Runs when | Use it for |
|---|---|---|
| **Advanced settings → Setup command** | Once before the test list | Dependencies or compilation shared by every test |
| A test's **Setup command** | Immediately before that test | Work needed only by one test |

Each setup and run command starts in a separate shell process. 

The assignment-level Setup command starts with a 120-second timeout. A per-test
command defaults to 10 seconds when its timeout is `0`; raise it when installing
packages or compiling a large project.

---

## A worked set

The suite behind this template is a cheap import guard plus the real pytest
suite. Add these under **Autograding tests**:

| Field | Import guard | Real suite |
|---|---|---|
| **Test name** | `Module imports` | `Pytest suite` |
| **Test type** | Run command | Python (pytest) |
| **Setup command** | — | `python3 -m pip install --quiet -r requirements.txt` |
| **Run command** | `python3 -c "import src.stats"` | `python3 -m pytest -q tests/test_stats.py` |
| **Required exit code** | `0` | — |
| **Timeout** | `10` | `120` |
| **Points** | `1` | `12` |

Thirteen points. A student who breaks the import loses 1 and is told exactly
that; a student whose logic is wrong loses proportionally across the 12.

---

## Traps

**A broken import scores all-or-nothing.** If pytest cannot collect, it reports
zero cases and the runner falls back to exit-code scoring. The whole 12 points
vanish together. The 1-point import test is what turns this from a mystery into
a labeled failure.

**A zero-point test does not score.** It still runs and reports. This is useful
for advisory feedback but usually accidental, so review the point total before
saving the assignment.

**The default per-command timeout is 10 seconds.** Anything doing `pip install`
usually needs more. A timeout reads to students as a wrong answer.

**Each submission starts in a fresh grading environment.** Files and installed
packages persist between commands in that one run; data does not persist from
one student submission to the next. Do not depend on the clock or randomness
without a fixed seed. A flaky test is a grade appeal.

> [!CAUTION]
> **Never put secrets in a setup or test command.** These commands run while
> grading code the student controls, and that code can print anything the job
> can read.

---

## When declarative tests aren't enough

Reach for a hand-written autograder when you need partial credit inside a
single test, need to inspect files rather than run them, or want hidden tests.

The Web UI authors declarative tests but does not upload `autograder.py`. Open
your organization's private `classroom50` config repository on GitHub and add:

```
<classroom>/autograders/<assignment-slug>/autograder.py
```

That file takes precedence over the assignment's declarative tests. A
classroom-wide default lives at `<classroom>/autograder.py`. This is an advanced
workflow: start from the contract and examples in the
[Autograders wiki](https://github.com/foundation50/classroom50/wiki/Autograders)
rather than inventing the result format.

**Hidden tests, specifically:** do not add secret cases to the suite in the
template, because students receive that repo. Put them in `autograder.py` in
the config repo, which is never distributed. Weigh the cost: hidden tests move
failures from "I can reproduce this locally" to "I have to guess," which is a
real teaching decision, not just a technical one.


---

## Before you hand it to students

> [!CAUTION]
> Whatever you wrote, **push a deliberately wrong submission and confirm it
> comes back red.** A green run is exactly what an autograded assignment with
> no tests can produce. See
> [Getting started with the Web UI, step 7](getting-started-web.md#step-7--prove-it-actually-grades).
