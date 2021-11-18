"""Use a generated list of papers and filter by a keyword."""

import json
from pathlib import Path

from rich.console import Console

from collector.finder import Finder

DEFAULT_PATH = Path.cwd() / 'output'
INPUT_FILE = DEFAULT_PATH / 'papers.json'
OUTPUT_FILE = DEFAULT_PATH / 'papers_filtered.json'

console = Console()


def main():
    """Run main function."""
    keywords = ['texture']

    with open(INPUT_FILE, 'r') as fil:
        papers = json.load(fil)

    fin = Finder()
    fin.papers = papers
    fin.filter_keywords(keywords)
    fin.save_papers(OUTPUT_FILE)
    console.log('Total papers: {0}'.format(len(fin.papers)))


if __name__ == '__main__':
    main()
