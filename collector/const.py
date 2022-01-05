"""Constants for the collector."""

from pathlib import Path

OUTPUT_FILE = Path.cwd() / 'output' / 'papers.json'
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
