"""Behavioral tests for both project modes, reference rendering and safe updates."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SKILL_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = SKILL_ROOT / "scripts" / "init_project.py"


class InitializeProjectTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="algorithm-skill-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def run_initializer(self, destination=None, mode="new", code_root=None, topics=None, script=SCRIPT):
        command = [sys.executable, str(script), "--mode", mode, "--name", "相机控制"]
        if destination is not None:
            command += ["--output", str(destination)]
        if code_root is not None:
            command += ["--code-root", str(code_root)]
        if topics is not None:
            command += ["--topics", topics]
        return subprocess.run(command, capture_output=True, text=True, encoding="utf-8")

    def source_snapshot(self):
        files = [SKILL_ROOT / "SKILL.md"]
        files.extend(path for path in (SKILL_ROOT / "references").rglob("*") if path.is_file())
        return {path.relative_to(SKILL_ROOT).as_posix(): path.read_bytes() for path in files}

    def test_new_project_creates_only_initial_topics_without_fake_code_or_nodes(self):
        before = self.source_snapshot()
        destination = self.root / "独立项目"
        completed = self.run_initializer(destination)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(
            {path.name for path in destination.iterdir()},
            {"README.md", "project.md", "0-problem.md", "1-design.md"},
        )
        project = (destination / "project.md").read_text(encoding="utf-8")
        self.assertIn("相机控制", project)
        self.assertIn("尚无代码", project)
        self.assertNotIn("N001", project)
        self.assertIn("解决思路", (SKILL_ROOT / "references" / "1-design.md").read_text(encoding="utf-8"))
        self.assertNotIn("本文件为 skill", (destination / "1-design.md").read_text(encoding="utf-8"))
        self.assertFalse((destination / "AGENTS.md").exists())
        self.assertFalse((destination / "code").exists())
        self.assertFalse((destination / "experiments").exists())
        self.assertEqual(before, self.source_snapshot())

    def test_existing_code_defaults_to_notes_subdirectory_and_keeps_originals(self):
        code = self.root / "existing-code"
        code.mkdir()
        originals = {
            "README.md": b"User's repository introduction.\n",
            "AGENTS.md": b"Existing engineering rules.\n",
            "train.py": b"raise RuntimeError('This file must never be executed')\n",
            "settings.json": b'{"steps": 4}\n',
        }
        for name, payload in originals.items():
            (code / name).write_bytes(payload)
        completed = self.run_initializer(mode="existing-code", code_root=code, topics="eval")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        notes = code / "docs"
        self.assertEqual(Path(result["output"]), notes)
        self.assertEqual({path.name for path in notes.iterdir()}, {"README.md", "project.md", "3-eval.md"})
        self.assertIn("| 代码位置 | .. |", (notes / "project.md").read_text(encoding="utf-8"))
        for name, payload in originals.items():
            self.assertEqual((code / name).read_bytes(), payload)
        self.assertFalse((notes / "code").exists())

    def test_explicit_code_root_output_preserves_readme_and_agents(self):
        code = self.root / "same-root"
        code.mkdir()
        (code / "README.md").write_bytes(b"Keep my root README.\n")
        (code / "AGENTS.md").write_bytes(b"Keep my root AGENTS.\n")
        completed = self.run_initializer(code, mode="existing-code", code_root=code, topics="none")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual((code / "README.md").read_bytes(), b"Keep my root README.\n")
        self.assertEqual((code / "AGENTS.md").read_bytes(), b"Keep my root AGENTS.\n")
        self.assertIn("| 代码位置 | . |", (code / "project.md").read_text(encoding="utf-8"))

    def test_separate_notes_directory_points_to_existing_code_without_copying(self):
        code = self.root / "code"
        code.mkdir()
        (code / "infer.py").write_text("pass\n", encoding="utf-8")
        notes = self.root / "notes"
        completed = self.run_initializer(notes, mode="existing-code", code_root=code, topics="data,eval")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("| 代码位置 | ../code |", (notes / "project.md").read_text(encoding="utf-8"))
        self.assertFalse((notes / "infer.py").exists())
        self.assertFalse((notes / "0-problem.md").exists())

    def test_repeat_preserves_facts_and_updates_only_managed_navigation(self):
        destination = self.root / "existing"
        self.assertEqual(self.run_initializer(destination).returncode, 0)
        fact = b"Existing confirmed problem statement.\n"
        (destination / "0-problem.md").write_bytes(fact)
        project = (destination / "project.md").read_bytes() + b"\nActual historical node N001.\n"
        (destination / "project.md").write_bytes(project)
        readme = (destination / "README.md").read_text(encoding="utf-8") + "\nUser-maintained notes must survive.\n"
        (destination / "README.md").write_text(readme, encoding="utf-8")
        completed = self.run_initializer(destination, topics="problem,delivery")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["created"], ["4-delivery.md"])
        self.assertEqual(result["updated"], ["README.md"])
        self.assertEqual((destination / "0-problem.md").read_bytes(), fact)
        self.assertEqual((destination / "project.md").read_bytes(), project)
        updated_readme = (destination / "README.md").read_text(encoding="utf-8")
        self.assertIn("User-maintained notes must survive.", updated_readme)
        self.assertIn("4-delivery.md", updated_readme)
        again = self.run_initializer(destination, topics="problem,delivery")
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertEqual(json.loads(again.stdout)["created"], [])
        self.assertEqual(json.loads(again.stdout)["updated"], [])

    def test_references_are_the_only_source_of_generated_sections(self):
        clone = self.root / "skill-copy"
        (clone / "scripts").mkdir(parents=True)
        shutil.copy2(SCRIPT, clone / "scripts" / "init_project.py")
        shutil.copytree(SKILL_ROOT / "references", clone / "references")
        design = clone / "references" / "1-design.md"
        design.write_text(design.read_text(encoding="utf-8") + "\n<!-- project-section -->\n## Newly maintained section\n\nInstruction text must not be copied.\n", encoding="utf-8")
        destination = self.root / "rendered"
        completed = self.run_initializer(destination, topics="design", script=clone / "scripts" / "init_project.py")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        rendered = (destination / "1-design.md").read_text(encoding="utf-8")
        self.assertIn("## Newly maintained section", rendered)
        self.assertNotIn("Instruction text must not be copied.", rendered)
        self.assertFalse((clone / "assets").exists())

    def test_all_topics_are_available_without_creating_experiments(self):
        destination = self.root / "all"
        completed = self.run_initializer(destination, topics="all")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(len(json.loads(completed.stdout)["created"]), 7)
        self.assertFalse((destination / "experiments").exists())

    def test_skill_root_and_nested_paths_are_rejected(self):
        before = self.source_snapshot()
        nested = SKILL_ROOT / "references" / "forbidden-project-output"
        for destination in (SKILL_ROOT, nested, SKILL_ROOT / "references" / ".."):
            with self.subTest(destination=destination):
                self.assertNotEqual(self.run_initializer(destination).returncode, 0)
        self.assertFalse(nested.exists())
        self.assertEqual(before, self.source_snapshot())

    def test_existing_code_requires_a_real_external_directory(self):
        destination = self.root / "not-created"
        for source in (None, self.root / "missing", SKILL_ROOT):
            with self.subTest(source=source):
                completed = self.run_initializer(destination, mode="existing-code", code_root=source)
                self.assertNotEqual(completed.returncode, 0)
        self.assertFalse(destination.exists())

    def test_invalid_topics_or_new_mode_code_argument_do_not_create_output(self):
        destination = self.root / "not-created"
        code = self.root / "code"
        code.mkdir()
        self.assertNotEqual(self.run_initializer(destination, topics="unknown").returncode, 0)
        self.assertNotEqual(self.run_initializer(destination, code_root=code).returncode, 0)
        self.assertFalse(destination.exists())

    def test_document_conflict_is_detected_before_any_file_is_written(self):
        destination = self.root / "conflict"
        (destination / "0-problem.md").mkdir(parents=True)
        completed = self.run_initializer(destination)
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual({path.name for path in destination.iterdir()}, {"0-problem.md"})

    def test_incomplete_managed_navigation_is_not_overwritten(self):
        destination = self.root / "navigation"
        destination.mkdir()
        original = b"User content\n<!-- algorithm-project:docs:start -->\n"
        (destination / "README.md").write_bytes(original)
        completed = self.run_initializer(destination)
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual((destination / "README.md").read_bytes(), original)
        self.assertEqual({path.name for path in destination.iterdir()}, {"README.md"})

    def test_symbolic_link_to_skill_is_rejected(self):
        link = self.root / "skill-link"
        try:
            link.symlink_to(SKILL_ROOT, target_is_directory=True)
        except OSError as error:
            self.skipTest("Creating a symbolic link is unavailable: " + str(error))
        before = self.source_snapshot()
        self.assertNotEqual(self.run_initializer(link).returncode, 0)
        self.assertEqual(before, self.source_snapshot())


if __name__ == "__main__":
    unittest.main()
