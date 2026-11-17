#!/usr/bin/env python3
"""Build .devcontainer/lesson-checks.json from the lesson files.

    python tools/build_checks.py path/to/modules/1-install-load-and-query

It reads every lesson.mdx in order, pulls out each code block, runs the blocks
the way a student would, and records what they print. `lab-check --full`
replays the result inside the Codespace.

Where a lesson shows the expected output in a `text` block, that text is the
expectation, and this script stops if the code does not print it. Where a
lesson shows no output (a challenge answer, for example), the output observed
here is recorded instead.

Run it with a Python that has the pinned packages installed. Rerun it whenever
a lesson changes.
"""
import importlib.machinery
import importlib.util
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / ".devcontainer" / "lesson-checks.json"

# Setup commands a student may run but the check must not: they install
# packages, start an interactive prompt, or change the shell's own state.
SKIP_BASH = re.compile(r"^(pip install|python3 -m venv|source |mkdir relate-python)|^python$", re.M)
SAVE_AS = re.compile(r"[Ss]ave (?:this|it) as `([\w.]+)`")
FENCE = re.compile(r"^```(\w+)?( noRun)?\n(.*?)^```$", re.M | re.S)
ANNOTATED = re.compile(r"<AnnotatedCode.*?</AnnotatedCode>", re.S)
# Lessons 1 to 4 share one folder. Challenge 5 starts clean and 6 and 7 build on it.
FOLDER = {1: "lessons", 2: "lessons", 3: "lessons", 4: "lessons", 5: "challenge", 6: "challenge", 7: "challenge"}
NEEDS_PANDAS = re.compile(r"\bpandas\b|\.to_df\(")


def load_runner():
    path = str(REPO / ".devcontainer" / "bin" / "lab-check")
    loader = importlib.machinery.SourceFileLoader("lab_check", path)
    spec = importlib.util.spec_from_loader("lab_check", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def extract(module_dir):
    steps = []
    lessons = sorted((module_dir / "lessons").iterdir(), key=lambda p: int(p.name.split("-")[0]))
    for lesson in lessons:
        raw = (lesson / "lesson.yml").read_text()
        meta = {key: re.search(rf"^{key}:\s*(.+)$", raw, re.M).group(1).strip() for key in ("title", "type", "order")}
        order = int(meta["order"])
        kind_word = "Challenge" if meta["type"] == "challenge" else "Lesson"
        title = f"{kind_word} {order}: {meta['title']}"
        text = (lesson / "lesson.mdx").read_text()
        excerpts = [(m.start(), m.end()) for m in ANNOTATED.finditer(text)]
        pandas_files = set()
        last = None
        for match in FENCE.finditer(text):
            lang, body = match.group(1), match.group(3)
            if any(start <= match.start() < end for start, end in excerpts):
                continue
            before = text[max(0, match.start() - 400):match.start()]
            if "```" in before:
                before = before[before.rfind("```") + 3:]
            base = {"lesson": lesson.name, "title": title, "dir": FOLDER[order]}
            if lang == "bash":
                last = None
                if SKIP_BASH.search(body):
                    continue
                first = body.strip().splitlines()[0]
                step = {**base, "kind": "bash", "label": first[:70], "body": body, "expect": None}
                if any(name in body for name in pandas_files):
                    step["needs"] = ["pandas", "pyarrow"]
                steps.append(step)
                last = step
            elif lang == "python":
                names = SAVE_AS.findall(before)
                if names:
                    step = {**base, "kind": "file", "name": names[-1], "label": names[-1], "body": body}
                    if NEEDS_PANDAS.search(body):
                        step["needs"] = ["pandas", "pyarrow"]
                        pandas_files.add(names[-1])
                    steps.append(step)
                    last = None
                else:
                    first = body.strip().splitlines()[0]
                    step = {**base, "kind": "repl", "label": f"prompt: {first[:60]}", "body": body, "expect": None}
                    steps.append(step)
                    last = step
            elif lang == "text" and last is not None:
                if "prompt" in before:
                    last = None  # a prompt to give an agent, not program output
                    continue
                last["expect"] = body
                last["source"] = "lesson"
                last = None
    return steps


def record(steps, runner):
    """Run every step. Check lesson expectations and record the rest."""
    work = Path(tempfile.mkdtemp(prefix="build-checks-"))
    namespaces = {}
    problems = 0
    try:
        for step in steps:
            cwd = work / step["dir"]
            cwd.mkdir(parents=True, exist_ok=True)
            output, error = runner.run_step(step, cwd, namespaces)
            if step["kind"] == "file":
                continue
            if error:
                problems += 1
                print(f"ERROR   {step['title']} | {step['label']}\n{error}")
            elif step.get("source") == "lesson":
                if output.strip() != step["expect"].strip():
                    problems += 1
                    print(f"MISMATCH {step['title']} | {step['label']}\nlesson shows:\n{step['expect']}\ncode printed:\n{output}")
            elif "object at 0x" in output or str(work) in output or "site-packages" in output:
                step["expect"] = None  # output changes from run to run, so only require success
            else:
                step["expect"] = output
                step["source"] = "recorded"
    finally:
        for namespace in namespaces.values():
            conn = namespace.get("conn")
            if conn is not None and hasattr(conn, "close"):
                try:
                    conn.close()
                except Exception:  # noqa: BLE001
                    pass
        shutil.rmtree(work, ignore_errors=True)
    return problems


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip())
        return 2
    module_dir = Path(sys.argv[1]).resolve()
    runner = load_runner()
    steps = extract(module_dir)
    problems = record(steps, runner)
    if problems:
        print(f"\n{problems} problem(s). {OUT.name} was not written.")
        return 1
    import relate

    data = {
        "generated_from": module_dir.name,
        "relate_db": relate.__version__,
        "python": ".".join(map(str, sys.version_info[:3])),
        "steps": steps,
    }
    OUT.write_text(json.dumps(data, indent=2) + "\n")
    checked = sum(1 for s in steps if s["kind"] != "file")
    from_lesson = sum(1 for s in steps if s.get("source") == "lesson")
    recorded = sum(1 for s in steps if s.get("source") == "recorded")
    print(f"wrote {OUT.relative_to(REPO)}: {len(steps)} steps, {checked} run, "
          f"{from_lesson} compared with lesson text, {recorded} recorded, "
          f"{checked - from_lesson - recorded} run for success only")
    return 0


if __name__ == "__main__":
    sys.exit(main())
