"""Chapter 15: set up a new analysis project folder with the standard layout.

Usage (from the repository folder):
    python scripts/new_project.py "Northern on-time" --root projects
"""
import argparse
import re
import shutil
from datetime import date
from pathlib import Path

FOLDERS = [
    "01_brief",
    "02_data/raw",        # extracts exactly as received; never edited
    "02_data/clean",      # outputs of your cleaning code
    "03_code",
    "04_qa",
    "05_outputs",
    "06_handover",
]

# which blank template goes into which folder
TEMPLATES = {
    "01_project_brief.docx": "01_brief",
    "03_data_dictionary.xlsx": "02_data",
    "05_source_register.xlsx": "02_data",
    "07_qa_checklist.xlsx": "04_qa",
    "09_assumptions_decisions_log.xlsx": "04_qa",
    "11_handover_document.docx": "06_handover",
}


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def new_project(name: str, root: Path, templates: Path) -> Path:
    folder = root / f"{date.today():%Y-%m}_{slugify(name)}"
    if folder.exists():
        raise SystemExit(f"{folder} already exists")
    for sub in FOLDERS:
        (folder / sub).mkdir(parents=True)
    for template, sub in TEMPLATES.items():
        src = templates / template
        if src.exists():
            shutil.copy(src, folder / sub / template)
    (folder / "README.md").write_text(
        f"# {name}\n\nStarted: {date.today():%d %B %Y}\n\n"
        "Brief: 01_brief/01_project_brief.docx\n"
        "To rerun: see 06_handover/11_handover_document.docx\n",
        encoding="utf-8",
    )
    return folder


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--root", default="projects")
    parser.add_argument("--templates", default="templates/blank")
    args = parser.parse_args()
    folder = new_project(args.name, Path(args.root), Path(args.templates))
    for path in sorted(folder.rglob("*")):
        depth = len(path.relative_to(folder).parts) - 1
        print("    " * depth + path.name + ("/" if path.is_dir() else ""))
