"""Relevant paper finder."""

import json
from pathlib import Path

from collector.client import Client
from collector.console import console


class Finder(object):
    """Relevant paper finder class."""

    def __init__(self, seed: str):
        """Initialize relevant paper finder.

        Args:
            seed: The seed paper to start the search from.
        """
        self.seed = seed

    def init(self):
        """Initialize relevant paper finder."""
        self.client = Client()
        self.papers = [self.client.get_paper(self.seed)]

    def fill_missing(self):
        """Fill missing data with defaults."""
        for paper in self.papers:
            if paper['year'] is None:
                paper['year'] = 0
            if paper['abstract'] is None:
                paper['abstract'] = ''
            if paper['title'] is None:
                paper['title'] = ''

    def collect(self):
        """Get related papers."""
        console.log('Collecting related papers.')
        console.log('Before collection: {0}'.format(len(self.papers)))

        res = []
        for paper in self.papers:
            console.log(
                'Getting papers related to "{0}"'.format(paper['title']),
            )
            res += self.client.get_references(paper['externalIds']['DOI'])
            res += self.client.get_citations(paper['externalIds']['DOI'])
        self.papers += res
        self.fill_missing()

        console.log('After collection: {0}'.format(len(self.papers)))

    def filter_year(self, year: int) -> list:
        """Filter papers by year.

        Args:
            year: The year to filter by.
        """
        console.log('Filtering papers by year.')
        console.log('Before filtering: {0}'.format(len(self.papers)))

        res = []
        for paper in self.papers:
            if paper['year'] >= year:
                res.append(paper)
        self.papers = res

        console.log('After filtering: {0}'.format(len(self.papers)))

    def filter_keywords(self, keywords: list):
        """Filter papers by keyword.

        Args:
            keywords: The keywords to filter by.
        """
        console.log('Filtering papers by keywords.')
        console.log('Before filtering: {0}'.format(len(self.papers)))

        res = []
        for paper in self.papers:
            console.log('Matching keywords in "{0}"'.format(paper['title']))
            for keyword in keywords:
                if keyword in paper['title'] or keyword in paper['abstract']:
                    res.append(paper)
                    break

        self.papers = res

        console.log('After filtering: {0}'.format(len(self.papers)))

    def filter_duplicates(self):
        """Filter duplicate papers."""
        console.log('Filtering duplicate papers.')
        console.log('Before filtering: {0}'.format(len(self.papers)))

        res = []
        dois = []
        for paper in self.papers:
            try:
                doi = paper['externalIds']['DOI']
            except Exception:
                console.log('No DOI for paper: "{0}"'.format(paper['title']))
                continue
            if doi not in dois:
                res.append(paper)
                dois.append(doi)

        self.papers = res

        console.log('After filtering: {0}'.format(len(self.papers)))

    def save_papers(self, path: str):
        """Save papers to file.

        Args:
            path: The path to save the papers to.
        """
        path = Path(path) / 'papers.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as fout:
            json.dump(self.papers, fout)
