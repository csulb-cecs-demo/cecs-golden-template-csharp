# Governance — the recommended baseline

How to adapt this template for your course, and what the task force recommends
keeping along the way.

> [!IMPORTANT]
> **None of this is mandatory for any faculty member.**
>
> The Chair was explicit on this point: the golden template is offered as a
> solid guideline, a best practice, not as policy. It does not replace any
> course policy, and a course that ignores every recommendation below is not
> doing anything wrong.
>
> What follows is advice with reasons attached, so you can judge which parts
> apply to you. If a reason does not fit your course, the recommendation
> does not either.

---

## The idea

**Your content is yours. Structure is worth sharing.**

What you teach, in what language, weighted how you like, is nobody's business
but yours. The part worth converging on is smaller: where a student looks for
instructions, whether their work is checked automatically, whether AI use gets
disclosed the same way twice.

A student taking four CECS courses currently meets four conventions. Shrinking
that to one is the only thing this baseline is trying to do, and it is worth
doing only for as long as it is actually helping.

## The five recommendations

| ID | Recommendation | Why we recommend it |
|---|---|---|
| **CS-1** | Keep `VERIFICATION-LOG.md` and its Tools / Verification / Attestation sections | A disclosure record only helps if it looks the same across courses. A student who meets three formats in one term learns the format, not the habit. |
| **CS-2** | Keep real test files in `tests/` | An empty suite reports success. That is the failure this template was built around. |
| **CS-3** | Keep a workflow on `push` / `pull_request` | Students find out their work broke immediately rather than when you tell them. Fewer office hours that open with "it didn't work." |
| **CS-4** | Keep student instructions in `docs/` | Predictable location across courses. |
| **CS-5** | Keep a README that orients someone | A one-line stub helps nobody. This project's own config README started that way. |

Each looks only at whether something **exists**. None inspects your course
content, and none ever will.

### When a recommendation doesn't fit

Plenty of legitimate courses will break several of these:

- **Grading by in-person demo?** CS-3 is noise for you.
- **Instructions in Canvas?** CS-4 doesn't apply.
- **A course where AI use is banned outright and enforced differently?** CS-1
  may be redundant.

> [!TIP]
> There is no exception process, because there is nothing to get an exception
> from. Skip what doesn't fit and move on.
>
> If you think a recommendation is wrong in general, not just for your course,
> that's worth raising, since one that fits your course badly probably fits
> three others badly too. The May Tech Review is the natural venue.

## Everything else is yours

Explicitly:

- **The exercise.** Replace `src/`, `tests/`, and `docs/` wholesale.
- **The language.** Python is the sample, not the point. Node, Java, C, Go: the
  grading contract is "a command that exits non-zero on failure."
- **Test count and weighting.** Case count is your rubric.
- **Performance thresholds**, or dropping the perf check entirely.
- **Due dates, repo naming, branch policy, all prose.**
- **Anything you add:** linters, type checks, extra workflows, more docs.

The baseline has nothing to say about what you add, only about what the
template started with.

## Adapting the template

1. **Use this template** on
   [cecs-golden-template-python](https://github.com/Giacalone-CECS/cecs-golden-template-python).
2. Replace `src/`, `tests/`, and `docs/assignment.md` with your content.
3. Keep or rewrite `VERIFICATION-LOG.md` as suits your course.
4. Push. The self-check reports what drifted. **It will not fail your build.**
5. Wire up grading. See Getting started with the
   [Web UI](getting-started-web.md) or the [CLI](getting-started.md).

Run it yourself any time:

```sh
python3 .github/scripts/check_core_standard.py            # advisory (default)
python3 .github/scripts/check_core_standard.py --strict   # exit 1 on gaps
python3 .github/scripts/check_core_standard.py --json     # machine-readable
```

> [!NOTE]
> **`--strict` is opt-in and it's for you, not for anyone else.** If you're
> handing a repo to a TA and want drift caught before it reaches students, add
> `--strict` to the run step in
> [`core-standard.yml`](../.github/workflows/core-standard.yml). Nobody else is
> asking you to.

## Keeping this useful

RFP-1 provides for an annual **Tech Review** each May. Good questions for it:

- Has a recommendation become busywork? Retire it. One nobody believes in
  teaches people to ignore the whole document.
- Is something now worth recommending that isn't here?
- Do the CI actions, toolchain pins, and thresholds still reflect practice?

Adoption path: **UGCC approval → Fall pilot with volunteer faculty →
consideration for Spring 2027.** The pilot is where recommendations that
sounded sensible meet courses that didn't fit them; that feedback is the point of
running one.

If you change a recommendation, update **both** this document and
`.github/scripts/check_core_standard.py` in the same change. They're two halves
of one description and shouldn't drift.

> [!NOTE]
> **Where this lives is worth settling.** The template currently sits in an
> individual faculty member's teaching organization with a single
> administrator. Fine for a prototype; less so for something the department
> leans on, since continuity would depend on one person's account. Worth
> deciding before any broader adoption.

## What this is not

- **Not policy.** It replaces no course policy and binds nobody.
- **Not a review of your course.** Not the exercise, not the difficulty, not
  the grading scheme.
- **Not a gate.** The check is advisory; it makes drift visible, which is the
  opposite of preventing it.
- **Not a grading input.** It looks at repository structure and has no effect
  on any student's score.
