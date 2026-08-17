# Docs

Faculty guidance for Classroom 50 and for adapting this template.

The [template README](../README.md) covers this repository specifically: its
layout, its CI, and what to change when you make it yours. These guides cover
the surrounding system.

| Guide | For | Time |
|---|---|---|
| **[Getting started with the Web UI](getting-started-web.md)** | Never set up an autograder. Zero to a verified, working assignment in the browser. | ~45 min first time |
| **[Getting started with the CLI](getting-started.md)** | The same path using `gh teacher` and `gh student`. | ~45 min first time |
| **[Writing tests with the Web UI](writing-tests-web.md)** | Building and weighting tests in the assignment form, plus advanced and portable options. | ~20 min |
| **[Writing tests with the CLI](writing-tests.md)** | The same grading model using `gh teacher` and JSON specs. | ~20 min |
| **[Troubleshooting](troubleshooting.md)** | Something is broken. Symptom → diagnosis → fix. | as needed |
| **[Governance](governance.md)** | Adapting the template for your course. The recommended baseline is advisory; nothing here is mandatory. | ~10 min |
| **[Performance sanity check](../perf/README.md)** | Load testing a service-building assignment. Opt-in. | ~10 min |
| [Sample assignment](assignment.md) | The student-facing instructions shipped with this template. Replace with your own. | — |

## If you read nothing else

> [!CAUTION]
> An assignment with no grading configured reports **0/0, status success**:
> green on every submission, including an empty one. A passing run is therefore
> not evidence that grading works; it is also exactly what a completely
> unconfigured assignment produces.
>
> **Before handing any assignment to students, push a deliberately wrong
> submission and confirm it comes back red.**

## Upstream

Classroom 50 itself is documented at
[foundation50/classroom50](https://github.com/foundation50/classroom50/wiki):
[Installation](https://github.com/foundation50/classroom50/wiki/Installation),
[Web Teacher Guide](https://github.com/foundation50/classroom50/wiki/Web-Teacher-Guide),
[CLI Teacher Guide](https://github.com/foundation50/classroom50/wiki/CLI-Teacher-Guide),
[Autograders](https://github.com/foundation50/classroom50/wiki/Autograders).
These guides cover the parts that wiki assumes you already know, plus the
CSULB-specific setup.

> [!NOTE]
> Org-specific internals (the grading workflows, roster, and collected scores)
> live in the private `Giacalone-CECS/classroom50` config repo. Nothing in these
> guides depends on access to it.
