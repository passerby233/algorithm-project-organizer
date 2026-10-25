#!/usr/bin/env python3
"""Initialize project notes from references, preserving existing code and documents."""

import argparse
import json
import os
from pathlib import Path
import re
import sys


SKILL_ROOT = Path(__file__).resolve().parent.parent
REFERENCE_ROOT = SKILL_ROOT / "references"
DOCUMENTS = {
    "problem": "0-problem.md",
    "design": "1-design.md",
    "data": "2-data.md",
    "eval": "3-eval.md",
    "delivery": "4-delivery.md",
}
NAV_START = "<!-- algorithm-project:docs:start -->"
NAV_END = "<!-- algorithm-project:docs:end -->"


def within(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def read_reference(filename):
    return (REFERENCE_ROOT / filename).read_text(encoding="utf-8")


def title_of(text):
    match = re.search(r"^# (.+)$", text, re.MULTILINE)
    if not match:
        raise ValueError("Reference has no document title.")
    return match.group(1).strip()


def render_topic(filename):
    text = read_reference(filename)
    headings = re.findall(r"<!-- project-section -->[ \t]*\r?\n(#{2,3} .+)", text)
    if not headings:
        raise ValueError("Reference has no marked output sections: " + filename)
    parts = ["# " + title_of(text)]
    for heading in headings:
        heading = re.sub(r"：待填写.*$", "", heading).strip()
        parts.append(heading + "\n\n待整理。")
    return "\n\n".join(parts) + "\n"


def reference_table(text, marker):
    if text.count(marker) != 1:
        raise ValueError("Reference must contain exactly one " + marker)
    lines = text.split(marker, 1)[1].splitlines()
    table = []
    for line in lines:
        if not line.strip() and not table:
            continue
        if line.startswith("|"):
            table.append(line)
        else:
            break
    if len(table) < 2:
        raise ValueError("Reference marker has no table: " + marker)
    return table


def cell(value):
    return str(value).replace("\r", " ").replace("\n", " ").replace("|", "&#124;")


def render_project(name, mode, code_root, destination):
    text = read_reference("project.md")
    code_location = "尚无代码"
    if code_root is not None:
        try:
            code_location = os.path.relpath(code_root, destination).replace("\\", "/")
        except ValueError:
            code_location = code_root.as_posix()
    values = {
        "项目名称": name or "待确认",
        "项目来源": "从零开始" if mode == "new" else "已有代码",
        "代码位置": code_location,
    }
    overview = reference_table(text, "<!-- project-overview -->")
    rendered = []
    for line in overview:
        cells = [part.strip() for part in line.strip("|").split("|")]
        if len(cells) == 2 and cells[0] in values:
            line = "| " + cells[0] + " | " + cell(values[cells[0]]) + " |"
        rendered.append(line)
    index = reference_table(text, "<!-- project-node-index -->")
    return (
        "# " + title_of(text) + "\n\n## 项目概况\n\n"
        + "\n".join(rendered)
        + "\n\n## 节点索引\n\n" + "\n".join(index)
        + "\n\n## 实际节点记录\n\n尚无实际节点。\n"
    )


def normalize_topics(topics):
    if topics is None:
        return ["problem", "design"]
    requested = [part.strip() for part in topics.split(",") if part.strip()]
    if requested == ["all"]:
        return list(DOCUMENTS)
    if requested in ([], ["none"]):
        return []
    unknown = set(requested) - set(DOCUMENTS)
    if unknown:
        raise ValueError("Unknown topics: " + ", ".join(sorted(unknown)))
    return [key for key in DOCUMENTS if key in requested]


def safe_target(destination, filename):
    target = destination / filename
    resolved = target.resolve()
    if within(resolved, SKILL_ROOT) or not within(resolved, destination):
        raise ValueError("A project path redirects outside the output or into the skill.")
    if target.exists() and not target.is_file():
        raise ValueError("An expected document is an existing directory: " + str(target))
    return target


def navigation(destination, planned_files):
    rows = ["| 文件 | 内容 |", "| --- | --- |", "| [project.md](project.md) | 项目概况与实际进展节点 |"]
    for filename in DOCUMENTS.values():
        if filename in planned_files or (destination / filename).is_file():
            rows.append("| [" + filename + "](" + filename + ") | " + title_of(read_reference(filename)) + " |")
    for experiment in sorted((destination / "experiments").glob("EXP-*.md")):
        if experiment.is_file():
            link = experiment.relative_to(destination).as_posix()
            rows.append("| [" + experiment.stem + "](" + link + ") | 实验记录 |")
    return NAV_START + "\n" + "\n".join(rows) + "\n" + NAV_END


def initialize(output=None, project_name=None, mode="new", code_root=None, topics=None):
    if mode not in ("new", "existing-code"):
        raise ValueError("Mode must be new or existing-code.")
    source = None
    if mode == "existing-code":
        if code_root is None:
            raise ValueError("Existing-code mode requires --code-root.")
        source = Path(code_root).expanduser().resolve()
        if not source.is_dir():
            raise ValueError("Code root must be an existing directory.")
        if within(source, SKILL_ROOT):
            raise ValueError("Code root must be outside the skill directory.")
        output = output or source / "docs"
    elif code_root is not None:
        raise ValueError("Use existing-code mode when providing a code root.")
    if output is None:
        raise ValueError("New-project mode requires --output.")
    destination = Path(output).expanduser().resolve()
    if within(destination, SKILL_ROOT):
        raise ValueError("Project output must be outside the skill directory.")
    if destination.exists() and not destination.is_dir():
        raise ValueError("Project output must be a directory.")
    for parent in destination.parents:
        if parent.exists() and not parent.is_dir():
            raise ValueError("Output path has a parent that is a file.")

    selected = normalize_topics(topics)
    filenames = ["project.md"] + [DOCUMENTS[key] for key in selected]
    targets = {filename: safe_target(destination, filename) for filename in filenames + ["README.md"]}
    payloads = {}
    preserved = []
    for filename in filenames:
        if targets[filename].exists():
            preserved.append(filename)
        elif filename == "project.md":
            payloads[filename] = render_project(project_name, mode, source, destination)
        else:
            payloads[filename] = render_topic(filename)

    nav = navigation(destination, filenames)
    readme = targets["README.md"]
    readme_change = None
    if not readme.exists():
        payloads["README.md"] = (
            "# " + cell(project_name or "算法项目")
            + "\n\n项目信息与代码位置见 project.md；主题文档按已有资料逐步补充。\n\n"
            + nav + "\n"
        )
    else:
        original = readme.read_bytes()
        try:
            text = original.decode("utf-8")
        except UnicodeDecodeError:
            text = ""
        start_count = text.count(NAV_START)
        end_count = text.count(NAV_END)
        if start_count or end_count:
            if start_count != 1 or end_count != 1 or text.index(NAV_END) < text.index(NAV_START):
                raise ValueError("README managed navigation markers are incomplete or duplicated.")
            updated = text[:text.index(NAV_START)] + nav + text[text.index(NAV_END) + len(NAV_END):]
            if updated != text:
                readme_change = (original, updated.encode("utf-8"))
        if readme_change is None:
            preserved.append("README.md")

    created = []
    updated = []
    for filename, payload in payloads.items():
        target = safe_target(destination, filename)
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            with target.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(payload)
        except FileExistsError:
            preserved.append(filename)
        else:
            created.append(filename)
    if readme_change is not None:
        safe_target(destination, "README.md")
        original, replacement = readme_change
        if readme.read_bytes() != original:
            raise ValueError("README changed during initialization; retry without replacing user edits.")
        readme.write_bytes(replacement)
        updated.append("README.md")

    return {
        "output": str(destination),
        "mode": mode,
        "code_root": str(source) if source is not None else None,
        "topics": selected,
        "created": created,
        "updated": updated,
        "preserved": preserved,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", required=True, choices=("new", "existing-code"))
    parser.add_argument("--output", help="Documentation directory, not project root; required for new projects (normally PROJECT_ROOT/docs), defaults to CODE_ROOT/docs for existing code")
    parser.add_argument("--code-root", help="Existing code directory; its contents are not moved or executed")
    parser.add_argument("--name", help="Project name for newly created documents")
    parser.add_argument("--topics", help="Comma-separated problem,design,data,eval,delivery; defaults to problem,design; also all or none")
    args = parser.parse_args()
    try:
        result = initialize(args.output, args.name, args.mode, args.code_root, args.topics)
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
