#!/usr/bin/env python3
"""Validate a base-convention checkpoint; optionally commit the staged snapshot."""

import argparse
import os
import subprocess
import sys

REFS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references")
FORMAT_HINT = ("Format: <type>: [<ticket>][<author>] <RED|GREEN> <lowercase imperative description>. "
               f"Rules: {os.path.join(REFS, 'commit-gate.md')}")
NEXT_STEP = {
    "RED": "Next: implement the minimum behavior, rerun the same scenario, then commit GREEN.",
    "GREEN": ("Next: read " + os.path.join(REFS, "design-assessment-after-green.md") +
              " and assess the design (and red-green-refactor.md if work is selected) "
              "before declaring core completion."),
}


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", repo, *args], check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout.rstrip("\n")


def validate(subject, ticket, author, kind, phase):
    for label, value in (("ticket", ticket), ("author", author)):
        if (not value or value != value.strip()
                or any(c in value for c in "[]<>\r\n")
                or any(ord(c) < 32 for c in value)):
            raise ValueError(f"{label} must be a resolved, nonempty single-line value")
    if phase == "RED" and kind != "test":
        raise ValueError("RED checkpoints require type test")
    prefix = f"{kind}: [{ticket}][{author}] {phase} "
    if not subject.startswith(prefix):
        raise ValueError(f"expected {prefix}<imperative description>")
    description = subject[len(prefix):]
    if (not description or not description[0].islower()
            or description != description.strip() or description.endswith(".")
            or any(c in description for c in "<>\r\n")
            or any(ord(c) < 32 for c in description)):
        raise ValueError("description must start lowercase, contain no placeholders/control "
                         "characters and have no trailing whitespace or period")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="target repository (default: cwd)")
    parser.add_argument("--ticket", required=True, help="ticket explicitly supplied by user")
    parser.add_argument("--type", dest="kind", required=True,
                        choices=("test", "feat", "fix", "refactor"))
    parser.add_argument("--phase", required=True, choices=("RED", "GREEN"))
    parser.add_argument("--subject", required=True)
    parser.add_argument("--commit", action="store_true",
                        help="commit staged changes only after validation, then verify HEAD")
    args = parser.parse_args()
    committed = False
    try:
        author = git(args.repo, "config", "user.name")
        validate(args.subject, args.ticket, author, args.kind, args.phase)
        if args.commit:
            result = git(args.repo, "commit", "-m", args.subject)
            committed = True
            sha = git(args.repo, "rev-parse", "HEAD")
            actual = git(args.repo, "show", "-s", "--format=%s", sha)
            print(result)
            print(f"Created checkpoint: {sha}\nActual subject: {actual}")
            validate(actual, args.ticket, author, args.kind, args.phase)
            if actual != args.subject:
                raise ValueError("a hook changed the validated subject")
            print("Checkpoint message verified.")
            print(NEXT_STEP[args.phase])
        else:
            print(f"Valid subject: {args.subject}")
        return 0
    except (ValueError, subprocess.CalledProcessError, OSError) as exc:
        detail = (exc.stderr.strip() or "Git command failed; check repository and user.name"
                  if isinstance(exc, subprocess.CalledProcessError) else str(exc))
        print(f"Checkpoint rejected: {detail}", file=sys.stderr)
        if not committed:
            print(FORMAT_HINT, file=sys.stderr)
        if committed:
            print("A commit was created; stop and report it. History was not rewritten.",
                  file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
