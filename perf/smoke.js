// Performance sanity check — RFP-1 "Definition of Done".
//
// Simulates 75 concurrent user interactions against a target service and
// enforces Pass/Fail thresholds. k6 exits non-zero when a threshold is
// breached, so the workflow step fails on its own — no extra gating logic.
//
// ============================================================================
// FACULTY: when to turn this on
// ============================================================================
//
//   TURN IT ON for assignments that build a service — a web app, a REST API,
//   a socket server. "Your API must serve 75 concurrent users under 200ms with
//   under 1% errors" is a real requirement and load testing is a job-ready
//   skill. This is where the check earns its place.
//
//   LEAVE IT OFF for assignments with no service — semaphores, buffer
//   overflow, crypto labs, plain library code. There is nothing to put under
//   load, and a green run against a toy target proves nothing.
//
//   It does NOT test the grading pipeline. GitHub Actions is not under stress
//   from a class: students work asynchronously over days, and 60 concurrent
//   jobs has been more than sufficient for sections of 67+. The capacity risk
//   worth watching is the org's monthly Actions MINUTES budget, which this
//   cannot measure. See perf/README.md.
//
// Repoint at your own service with the BASE_URL environment variable:
//   k6 run -e BASE_URL=http://localhost:8080 perf/smoke.js

import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:8080';

// FACULTY: the two thresholds are the RFP's verification criteria verbatim.
// `med<200`  -> median latency under 200 ms
// `rate<0.01` -> error rate under 1%
// Tighten them for your assignment if you like; do not silently loosen them,
// because the number in the syllabus is the contract with the student.
export const options = {
  thresholds: {
    http_req_duration: ['med<200'],
    http_req_failed: ['rate<0.01'],

    // Guards against a vacuous pass. A threshold over a metric with no samples
    // passes trivially, so a run that generated NO load — a script error, a
    // misconfigured stage, a target that was never reachable — would otherwise
    // report green with nothing behind it. Same failure shape as an assignment
    // with no `tests` block: the absence of evidence rendering as success.
    //
    // `count>100` is a floor, not a target: 75 VUs with 1s think time over a
    // 30s plateau produces ~2000 requests, so anything near 100 means the run
    // did not really happen.
    http_reqs: ['count>100'],

    // Makes the check() assertions gate the run. Checks are recorded but do
    // NOT fail a k6 run on their own — a service returning 200 with an empty
    // body would otherwise sail through both latency and error-rate
    // thresholds.
    checks: ['rate>0.99'],
  },

  // 75 concurrent virtual users, held at plateau. The short ramp exists so the
  // measured window is steady-state rather than cold-start — the plateau is
  // what the 75-concurrent requirement refers to.
  stages: [
    { duration: '10s', target: 75 }, // ramp to 75
    { duration: '30s', target: 75 }, // hold 75 concurrent  <-- the requirement
    { duration: '5s', target: 0 },   // ramp down
  ],
};

export default function () {
  const res = http.get(`${BASE_URL}/`);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'body is not empty': (r) => r.body && r.body.length > 0,
  });

  // Think time. Without it, 75 VUs hammer in a tight loop, which measures how
  // fast you can generate load rather than how the service behaves with 75
  // users on it.
  sleep(1);
}

// ---------------------------------------------------------------------------
// Summary report artifact (RFP: "generate a summary performance report
// artifact available in the GitHub Action build logs").
//
// Deliberately dependency-free. The usual approach imports textSummary from
// jslib.k6.io, which needs network access at run time and turns a transient
// CDN failure into a failed student grade. Everything below is computed from
// the summary object k6 already handed us.
// ---------------------------------------------------------------------------
function thresholdRows(data) {
  const rows = [];
  for (const [name, metric] of Object.entries(data.metrics || {})) {
    if (!metric.thresholds) continue;
    for (const [expr, result] of Object.entries(metric.thresholds)) {
      // k6 has reported this as `ok` and, in older builds, `passes`.
      const passed = result.ok !== undefined ? result.ok : !result.fails;
      rows.push({ metric: name, expr, passed });
    }
  }
  return rows;
}

function fmt(n, digits = 2) {
  return typeof n === 'number' ? n.toFixed(digits) : 'n/a';
}

export function handleSummary(data) {
  const dur = (data.metrics.http_req_duration || {}).values || {};
  const failed = (data.metrics.http_req_failed || {}).values || {};
  const reqs = (data.metrics.http_reqs || {}).values || {};
  const vus = (data.metrics.vus_max || {}).values || {};

  const rows = thresholdRows(data);
  const allPassed = rows.every((r) => r.passed);
  const errPct = (failed.rate || 0) * 100;

  const md = [
    '# Performance Sanity Check',
    '',
    `**Result: ${allPassed ? '✅ PASS' : '❌ FAIL'}**`,
    '',
    '## Thresholds (RFP verification criteria)',
    '',
    '| Metric | Threshold | Result |',
    '|---|---|---|',
    ...rows.map(
      (r) => `| \`${r.metric}\` | \`${r.expr}\` | ${r.passed ? '✅ pass' : '❌ **FAIL**'} |`
    ),
    '',
    '## Measurements',
    '',
    '| Measure | Value |',
    '|---|---|',
    `| Peak concurrent users (VUs) | ${vus.max ?? 'n/a'} |`,
    `| Total requests | ${reqs.count ?? 'n/a'} |`,
    `| Throughput | ${fmt(reqs.rate)} req/s |`,
    `| **Median latency** | **${fmt(dur.med)} ms** |`,
    `| p(95) latency | ${fmt(dur['p(95)'])} ms |`,
    `| Average latency | ${fmt(dur.avg)} ms |`,
    `| Max latency | ${fmt(dur.max)} ms |`,
    `| **Error rate** | **${fmt(errPct)}%** |`,
    '',
  ].join('\n');

  const text = [
    '=== Performance Sanity Check ===',
    `Result:            ${allPassed ? 'PASS' : 'FAIL'}`,
    `Peak VUs:          ${vus.max ?? 'n/a'}`,
    `Requests:          ${reqs.count ?? 'n/a'} (${fmt(reqs.rate)}/s)`,
    `Median latency:    ${fmt(dur.med)} ms   (threshold: < 200)`,
    `p(95) latency:     ${fmt(dur['p(95)'])} ms`,
    `Error rate:        ${fmt(errPct)}%       (threshold: < 1)`,
    '',
    ...rows.map((r) => `  [${r.passed ? 'PASS' : 'FAIL'}] ${r.metric}: ${r.expr}`),
    '',
  ].join('\n');

  return {
    stdout: text,                              // shows in the build log
    'perf-report.md': md,                      // job summary + artifact
    'perf-report.txt': text,                   // artifact
    'perf-summary.json': JSON.stringify(data, null, 2), // full raw metrics
  };
}
