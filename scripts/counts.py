"""Get citation counts for a set of papers."""

import json
from pathlib import Path

from rich.console import Console

from collector.client import Client

INPUT_PATH = Path.cwd() / 'output/papers.json'
OUTPUT_PATH = Path.cwd() / 'output/paper_counts.json'
console = Console()

DEFAULT_FIELDS = ','.join([
    'externalIds',
    'url',
    'title',
    'abstract',
    'year',
    'authors',
    'citationCount',
])


def load_papers(path: str = INPUT_PATH) -> list:
    """Load papers from json file.

    Args:
        path (str): Path to json file.

    Returns:
        list: List of papers.
    """
    with open(path, 'r') as fi:
        papers = json.load(fi)

    return papers


def main():
    """Run main function."""
    papers = load_papers()
    client = Client(fields=DEFAULT_FIELDS)
    res = []

    for paper in papers:
        console.log('Getting citations for "{0}"'.format(paper['title']))
        paper_data = client.get_paper(paper['externalIds']['DOI'])

        res.append({
            'doi': paper['externalIds']['DOI'],
            'citationCount': paper_data['citationCount'],
            'title': paper['title'],
        })

    # Sort by citation count
    res = sorted(res, key=lambda x: x['citationCount'], reverse=True)

    with open(OUTPUT_PATH, 'w+') as fout:
        json.dump(res, fout, indent=4, sort_keys=True)


if __name__ == '__main__':
    main()
