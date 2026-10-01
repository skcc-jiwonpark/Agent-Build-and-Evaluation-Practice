#!/usr/bin/env python3
"""Create a local, read-only text index for papers in references/."""

from __future__ import annotations

import shutil
import subprocess
import os
from pathlib import Path


# The skill is stored in workspace_seed/ and copied into workspace/ at runtime.
# Derive the project directory from the working directory so both locations use
# the same references/, outputs/, and work/ folders.
ROOT = Path(os.getenv("PRECURSOR_WORKSPACE_ROOT", Path.cwd())).resolve()
REFERENCES = ROOT / "references"
EXTRACTED = ROOT / "work" / "extracted"
OUTPUT = ROOT / "outputs" / "source_index.md"
KEYWORDS = ("precursor", "synthesis", "experimental", "supporting information")


def extract(pdf: Path) -> str:
    if not shutil.which("pdftotext"):
        raise RuntimeError("pdftotext is required. Install Poppler, then run again.")
    result = subprocess.run(
        ["pdftotext", str(pdf), "-"], text=True, capture_output=True, check=True
    )
    return result.stdout


def title_from(text: str, fallback: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    title_starts = ("explainable synthesizability", "synthesis-aware")
    direct_title = next((line for line in lines if line.lower().startswith(title_starts)), None)
    if direct_title:
        return direct_title
    ignored_prefixes = ("how to cite", "doi.org", "research article", "article")
    candidates = [
        line
        for line in lines
        if len(line) > 20 and not line.lower().startswith(ignored_prefixes)
    ]
    return candidates[0] if candidates else fallback


def main() -> None:
    EXTRACTED.mkdir(parents=True, exist_ok=True)
    rows: list[str] = ["# Source index", "", "This index is generated locally. Original PDFs are not modified.", ""]
    pdfs = sorted(REFERENCES.glob("*.pdf"))
    if not pdfs:
        rows.append("No PDF files found in `references/`.")
    for pdf in pdfs:
        text = extract(pdf)
        text_path = EXTRACTED / f"{pdf.stem}.txt"
        text_path.write_text(text, encoding="utf-8")
        counts = ", ".join(f"{word}: {text.lower().count(word)}" for word in KEYWORDS)
        rows.extend(
            [
                f"## {pdf.name}",
                f"- Detected title: {title_from(text, pdf.stem)}",
                f"- Extracted text: `work/extracted/{text_path.name}`",
                f"- Keyword counts: {counts}",
                "",
            ]
        )
    OUTPUT.write_text("\n".join(rows), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
