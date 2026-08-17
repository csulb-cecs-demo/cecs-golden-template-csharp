#!/usr/bin/env python3
"""Core Standard self-check — a best-practice baseline, not a rule.

============================================================================
NONE OF THIS IS MANDATORY.
============================================================================

The Chair was explicit: the golden template is offered to CECS faculty as a
solid guideline, not as policy. Nothing here binds anyone, this script has no
authority over your course, and a course that ignores every rule below is not
doing anything wrong.

What this is: a checklist you can run against your own repo to see whether it
still lines up with the baseline the task force recommends. Useful when you
have adapted the template heavily and want a second pair of eyes on what drifted
— nothing more.

ADVISORY BY DEFAULT. It reports and exits 0. If you *want* it to hold you to
the baseline in your own course, pass --strict and it will exit non-zero
instead. That choice is yours to make, per course, and the default assumes you
have not made it.

The rules below are written as data so you can read what is recommended without
reading Python. docs/governance.md is the human-readable half — keep them in
sync if you change either.

Deliberately language-agnostic: a course that adapts this to Node or Java
should still come out clean, so the test-suite rule matches conventions across
languages rather than assuming pytest.

Usage:
    python3 .github/scripts/check_core_standard.py            # advisory
    python3 .github/scripts/check_core_standard.py --strict    # exit 1 on gaps
    python3 .github/scripts/check_core_standard.py --json
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

# --------------------------------------------------------------------------
# THE RECOMMENDED BASELINE
#
# Each rule is something the task force recommends keeping, with the reason
# we recommend it. Anything not listed is entirely yours — the exercise, the
# language, the number of tests, the weighting, the thresholds, the prose.
#
# And the listed items are yours too. These are recommendations with reasons
# attached; if a reason does not apply to your course, the recommendation does
# not either. See docs/governance.md.
# --------------------------------------------------------------------------

TEST_FILE_PATTERNS = [
    "tests/**/test_*.py", "tests/**/*_test.py",        # Python
    "tests/**/*.test.js", "tests/**/*.spec.js",        # JavaScript
    "tests/**/*.test.ts", "tests/**/*.spec.ts",        # TypeScript
    "tests/**/*Test.java", "tests/**/Test*.java",      # Java
    "tests/**/*_test.go",                              # Go
    "tests/**/test_*.c", "tests/**/*_test.c",          # C
    "tests/**/*Test.cs", "tests/**/*Tests.cs",         # C#
]

VERIFICATION_LOG_SECTIONS = [
    "Tools used",
    "How you verified it",
    "Attestation",
]


def rule_verification_log() -> tuple[bool, str]:
    """CS-1: the AI-assistance disclosure record.

    Recommended because a consistent record of how students used AI is only
    useful if it looks the same across courses — a student who meets three
    different disclosure formats in one semester learns the format, not the
    habit. Reword it freely; the sections are what make it a record rather
    than a checkbox.
    """
    path = "VERIFICATION-LOG.md"
    if not os.path.isfile(path):
        return False, f"{path} not found — the recommended AI-disclosure record"
    text = open(path, encoding="utf-8", errors="replace").read()
    missing = [s for s in VERIFICATION_LOG_SECTIONS if s.lower() not in text.lower()]
    if missing:
        return False, f"{path} has no section matching: {', '.join(missing)}"
    return True, f"{path} present with the recommended sections"


def rule_test_suite() -> tuple[bool, str]:
    """CS-2: a test suite with something in it.

    Recommended because an empty suite reports success — the failure this
    template was built around. A directory alone is not the point; something a
    test runner would actually pick up is.
    """
    if not os.path.isdir("tests"):
        return False, "tests/ directory is missing"
    found = []
    for pattern in TEST_FILE_PATTERNS:
        found.extend(glob.glob(pattern, recursive=True))
    if not found:
        return False, (
            "tests/ contains no recognizable test files. Add tests, or extend "
            "TEST_FILE_PATTERNS in this script for your language."
        )
    return True, f"tests/ contains {len(found)} test file(s)"


def rule_ci_workflow() -> tuple[bool, str]:
    """CS-3: automated feedback on push.

    Recommended because without it students find out whether their work builds
    when you tell them, which is slower for them and more office hours for you.
    Plenty of good courses grade by demo instead — if that is yours, this rule
    does not apply.
    """
    workflows = glob.glob(".github/workflows/*.yml") + glob.glob(".github/workflows/*.yaml")
    if not workflows:
        return False, ".github/workflows/ has no workflow files"
    for wf in workflows:
        text = open(wf, encoding="utf-8", errors="replace").read()
        # Strip comment-only lines FIRST. A naive substring search matches the
        # commented-out `# push:` that perf.yml ships as an opt-in hint, which
        # would let a dispatch-only repo pass this rule — a false green on the
        # exact deliverable the rule exists to protect.
        live = "\n".join(
            ln for ln in text.splitlines() if not ln.lstrip().startswith("#")
        )
        if not re.search(r"^on\s*:", live, re.M):
            continue
        if re.search(r"^\s*(push|pull_request)\s*:", live, re.M):
            return True, f"CI workflow present ({os.path.basename(wf)} triggers on push/PR)"
    return False, (
        "no workflow triggers on push or pull_request "
        "(a workflow_dispatch-only repo gives students no feedback loop)"
    )


def rule_student_instructions() -> tuple[bool, str]:
    """CS-4: the student can find out what to do.

    Recommended so instructions live in a predictable place across courses. Any
    markdown under docs/ counts — this looks for the affordance, never at the
    prose. If your instructions live in Canvas, that is a fine answer and this
    rule is noise for you.
    """
    if not os.path.isdir("docs"):
        return False, "docs/ directory is missing"
    docs = glob.glob("docs/**/*.md", recursive=True)
    if not docs:
        return False, "docs/ contains no markdown files"
    return True, f"docs/ contains {len(docs)} document(s)"


def rule_readme() -> tuple[bool, str]:
    """CS-5: a README that orients someone.

    The 200-byte floor exists because a one-line stub is how this project's own
    config README started, and it was useless to everyone who found it.
    """
    if not os.path.isfile("README.md"):
        return False, "README.md is missing"
    size = os.path.getsize("README.md")
    if size < 200:
        return False, f"README.md is only {size} bytes — too thin to orient anyone"
    return True, f"README.md present ({size} bytes)"


RULES = [
    ("CS-1", "Verification Log", rule_verification_log),
    ("CS-2", "Test suite", rule_test_suite),
    ("CS-3", "CI workflow", rule_ci_workflow),
    ("CS-4", "Student instructions", rule_student_instructions),
    ("CS-5", "README", rule_readme),
]


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Self-check against the recommended baseline. Advisory by default."
    )
    ap.add_argument("--json", action="store_true", help="emit machine-readable results")
    ap.add_argument(
        "--strict",
        action="store_true",
        help="exit non-zero on gaps. Opt in per course if you want the guardrail.",
    )
    args = ap.parse_args()

    results = []
    for rule_id, name, fn in RULES:
        try:
            ok, detail = fn()
        except Exception as exc:  # a crashing rule must not read as a pass
            ok, detail = False, f"rule raised {type(exc).__name__}: {exc}"
        results.append({"id": rule_id, "name": name, "passed": ok, "detail": detail})

    aligned = all(r["passed"] for r in results)
    gaps = [r for r in results if not r["passed"]]

    if args.json:
        print(json.dumps(
            {"aligned": aligned, "strict": args.strict, "rules": results}, indent=2
        ))
    else:
        print("Core Standard self-check — recommended baseline, not a requirement")
        print("=" * 68)
        for r in results:
            mark = " ok " if r["passed"] else "note"
            print(f"  [{mark}] {r['id']} {r['name']}: {r['detail']}")
        print("=" * 68)
        if aligned:
            print("Matches the recommended baseline.")
        else:
            print(f"{len(gaps)} item(s) differ from the recommended baseline.")
            print("That may be exactly right for your course. See docs/governance.md")
            print("for what each recommendation is for, so you can decide.")
        if not args.strict and gaps:
            print("\nAdvisory run — exiting 0. Use --strict to make gaps fail.")

    # Advisory by default: differing from a recommendation is not an error.
    # --strict is opt-in, for faculty who want the baseline enforced in their
    # own course.
    return 1 if (args.strict and not aligned) else 0


if __name__ == "__main__":
    sys.exit(main())
