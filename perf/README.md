# Performance sanity check

An automated load test that drives **75 concurrent users** at a target service
and fails the build if median latency exceeds **200 ms** or the error rate
exceeds **1%**. Satisfies the RFP-1 "Performance Sanity Check" deliverable.

| File | What it is |
|---|---|
| `smoke.js` | The k6 script: 75 VUs, thresholds, report generation |
| `reference_service.py` | A stand-in target so it runs out of the box. Replace with your service. |
| `../.github/workflows/perf.yml` | The workflow. **Opt-in**; see below. |

## Running it

From the Actions tab: **Performance Sanity Check → Run workflow**. Leave the
target blank to use the bundled reference service, or supply a URL.

Locally:

```sh
python3 perf/reference_service.py &        # or start your own service
k6 run perf/smoke.js
k6 run -e BASE_URL=http://localhost:3000 perf/smoke.js   # your service
```

> [!TIP]
> Port 8080 is a popular default and may already be in use on your machine.
> `PORT=8099 python3 perf/reference_service.py` and pass the matching
> `BASE_URL`.

## When to turn it on

> [!IMPORTANT]
> **Enable it** for assignments that build a service: a web app, a REST API, a
> socket server. "Your API must serve 75 concurrent users under 200 ms with
> under 1% errors" is a real requirement, and load testing is a genuinely
> job-ready skill.
>
> **Leave it off** for assignments with no service: semaphores, buffer
> overflow, crypto labs, plain library code. There is nothing to put under
> load.

It ships opt-in (`workflow_dispatch` only). To enable it for an assignment,
uncomment the `push:` trigger in `perf.yml`.

Why opt-in rather than always-on: a green check that attests to nothing is
worse than no check. It devalues every real green badge next to it, and that is
[exactly how an autograder came to silently pass every submission](../docs/troubleshooting.md#everything-passes-including-work-that-should-fail).

## What it does not test

> [!WARNING]
> **This does not test the grading pipeline.** GitHub Actions is not under
> stress from a class. Students work asynchronously over days and weeks; the
> deadline spike never approaches simultaneous, and 60 concurrent jobs has been
> more than sufficient for sections of 67+.

The capacity risk worth watching for a large-enrollment course is the
organization's monthly Actions **minutes** budget, not concurrency. A workflow
on a per-push trigger can run a hundred-plus times for a single student across
a semester, and that is what exhausts a quota mid-term. This check cannot
measure it.

> [!TIP]
> **There is a direct lever for that.** Set the assignment's submission mode to
> `tag` and only `submit/*` tag pushes grade; a plain `git push` costs no
> Actions minutes at all. Students submit with `gh student submit`.
>
> ```sh
> gh teacher assignment add <org> <classroom> <slug> ... --submission-mode tag
> gh teacher assignment submission-mode <org> <classroom> <slug> tag   # retrofits existing repos
> ```
>
> The tradeoff is the feedback loop: students stop getting a result on every
> push, which is most of why CI is worth having. Reasonable middle ground is
> `every-push` for early low-enrollment labs and `tag` for the large sections
> where the minutes actually bite.

## The thresholds

```javascript
http_req_duration: ['med<200'],   // median latency < 200 ms
http_req_failed:   ['rate<0.01'], // error rate < 1%
http_reqs:         ['count>100'], // guard: the run actually generated load
checks:            ['rate>0.99'], // guard: responses were actually valid
```

The first two are the RFP's verification criteria verbatim. k6 exits non-zero
when any threshold is breached, so the workflow fails on its own.

The last two are guards, and they earn their place:

- **`http_reqs`**. A threshold over a metric with **no samples passes
  trivially**. Without this, a run that generated no load at all (script error,
  misconfigured stage, target never reachable) reports green with nothing
  behind it.
- **`checks`**. `check()` assertions are recorded but do **not** fail a k6 run
  on their own. A service returning `200 OK` with an empty body would sail
  through both latency and error-rate thresholds without this.

Both guards exist because *absence of evidence rendering as success* is the
same bug this template was built to fix.

## Verified behavior

Each of these was run, not assumed:

| Scenario | Result |
|---|---|
| Healthy target, 75 VUs | ✅ PASS, exit 0. 2,850 requests, 0.16 ms median, 0% errors |
| Latency threshold breached | ❌ FAIL, exit 99, breaching threshold named |
| Target unreachable | ❌ FAIL, exit 99, 100% error rate |
| No load generated | ❌ FAIL, exit 99. The `http_reqs` guard catches it |

## The report

`handleSummary()` writes three artifacts, uploaded by the workflow and retained
30 days:

| File | Contents |
|---|---|
| `perf-report.md` | Rendered into the **job summary**, readable without downloading anything |
| `perf-report.txt` | Plain text, also printed to the build log |
| `perf-summary.json` | Full raw k6 metrics |

Deliberately dependency-free. The common approach imports `textSummary` from
`jslib.k6.io`, which needs network access at run time. That turns a transient
CDN outage into a failed student grade.
