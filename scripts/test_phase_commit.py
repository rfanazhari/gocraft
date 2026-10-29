"""Exercise real Git checkpoints without touching the user's repository."""

from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("phase_commit.py")


class PhaseCommitTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        self.git("init", "-q")
        self.git("config", "user.name", "Alice Example")
        self.git("config", "user.email", "alice@example.test")
        (self.repo / "fixture").write_text("staged checkpoint\n")
        self.git("add", "fixture")
        self.subject = "test: [BLOG-002][Alice Example] RED cover blog values lifecycle and creation policy"

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.repo), *args], check=True,
                              text=True, capture_output=True, env=self.env).stdout.strip()

    def run_gate(self, subject=None, phase="RED", kind="test", commit=False, ticket="BLOG-002"):
        command = [sys.executable, str(SCRIPT), "--repo", str(self.repo),
                   "--ticket", ticket, "--type", kind, "--phase", phase,
                   "--subject", self.subject if subject is None else subject]
        if commit:
            command.append("--commit")
        return subprocess.run(command, text=True, capture_output=True, env=self.env)

    def test_reported_bad_subject_and_missing_author_never_create_commit(self):
        bad_subjects = [
            "test(blogs): [BLOG-002] RED cover blog values lifecycle and creation policy",
            "test: [BLOG-002] RED cover blog values lifecycle and creation policy",
            "test: [Alice Example][BLOG-002] RED cover blog values",
            "test: [BLOG-002][someone] RED cover blog values",
            "test: [BLOG-003][Alice Example] RED cover blog values",
            self.subject.replace(" RED ", " GREEN "),
            self.subject.replace("test:", "feat:"),
            self.subject.replace("[Alice Example]", "[Alice Example][blogs]"),
            self.subject + "\nbody",
            self.subject + ".",
            self.subject.replace("cover", "Cover"),
            "test: [BLOG-002][<author>] RED cover blog values",
        ]
        for subject in bad_subjects:
            with self.subTest(subject=subject):
                result = self.run_gate(subject, commit=True)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertFalse(any((self.repo / ".git/refs/heads").iterdir()))
                self.assertEqual(self.git("diff", "--cached", "--name-only"), "fixture")

    def test_validate_only_preserves_staging_and_does_not_commit(self):
        result = self.run_gate()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(any((self.repo / ".git/refs/heads").iterdir()))
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "fixture")

    def test_valid_commit_reports_actual_subject_and_sha(self):
        result = self.run_gate(commit=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git("show", "-s", "--format=%s"), self.subject)
        self.assertIn(self.git("rev-parse", "HEAD"), result.stdout)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "")

    def test_green_types_and_red_type_gate(self):
        for kind in ("test", "feat", "fix", "refactor"):
            with self.subTest(kind=kind):
                subject = f"{kind}: [BLOG-002][Alice Example] GREEN implement blog values"
                self.assertEqual(self.run_gate(subject, "GREEN", kind).returncode, 0)
                if kind != "test":
                    subject = subject.replace(" GREEN ", " RED ")
                    self.assertNotEqual(self.run_gate(subject, "RED", kind).returncode, 0)

    def test_hook_mutation_is_reported_without_rewriting_commit(self):
        hook = self.repo / ".git/hooks/commit-msg"
        hook.write_text('#!/bin/sh\nprintf "%s\\n" "test(blogs): [BLOG-002] RED cover blog values" > "$1"\n')
        hook.chmod(0o755)
        result = self.run_gate(commit=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("A commit was created", result.stderr)
        self.assertIn(self.git("rev-parse", "HEAD"), result.stdout)
        self.assertEqual(self.git("rev-list", "--count", "HEAD"), "1")
        self.assertEqual(self.git("show", "-s", "--format=%s"),
                         "test(blogs): [BLOG-002] RED cover blog values")

    def test_missing_author_blocks_commit(self):
        self.git("config", "--unset", "user.name")
        result = self.run_gate(commit=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(any((self.repo / ".git/refs/heads").iterdir()))


if __name__ == "__main__":
    unittest.main()
