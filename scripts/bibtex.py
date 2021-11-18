"""Generate bibtex enteries."""

import http
import json
import time
from pathlib import Path

import requests
from rich.console import Console

INPUT_PATH = Path.cwd() / 'output/papers.json'
OUTPUT_PATH = Path.cwd() / 'output/paper.bib'
console = Console()


def get_bibtex(doi: str) -> str:
    """Get bibtex entry for a paper.

    Args:
        doi (str): DOI of paper.

    Returns:
        str: Bibtex entry.
    """
    url = 'https://api.crossref.org/{0}/{1}/{2}'.format(
        'works',
        doi,
        'transform/application/x-bibtex',
    )

    resp = requests.get(url)
    if resp.status_code != http.HTTPStatus.OK:
        return None

    return resp.text


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


def clear_bibtex(path: str = OUTPUT_PATH):
    """Clear bibtex file.

    Args:
        path (str): Path to bibtex file.
    """
    with open(path, 'w+') as fo:
        fo.write('')


def append_bibtex(bibtex: str, path: str = OUTPUT_PATH):
    """Append bibtex to file.

    Args:
        path (str): Path to bibtex file.
        bibtex (str): Bibtex entry.
    """
    with open(path, 'a') as fon:
        fon.write(bibtex)
        fon.write('\n\n')


def main():
    """Run main function."""
    papers = load_papers()

    for paper in papers:
        console.log('Citing "{0}"'.format(paper['title']))

        try:
            doi = paper['externalIds']['DOI']
        except Exception:
            console.log(
                'No DOI found for "{0}".'.format(paper['title']),
                style='red',
            )
            continue

        bibtex = get_bibtex(doi)
        if bibtex is None:
            console.log(
                'No bibtex found for "{0}".'.format(paper['title']),
                style='red',
            )
            continue

        append_bibtex(bibtex)
        time.sleep(1)


if __name__ == '__main__':
    main()
