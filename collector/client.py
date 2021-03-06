"""API Client for semanticscholar."""

import http
import time

import requests
import requests_cache
from beartype import beartype

from collector.console import console

WAIT_SECS = 1.5
DEFAULT_FIELDS = ','.join([
    'externalIds',
    'url',
    'title',
    'abstract',
    'year',
    'authors',
])
CACHE_EXPIRE = 180
requests_cache.install_cache(
    'semanticscholar',
    backend='sqlite',
    expire_after=CACHE_EXPIRE,
)


class Client(object):
    """API Client for semanticscholar."""

    @beartype
    def __init__(self, fields: str = DEFAULT_FIELDS):
        """Initialize the client.

        Args:
            fields (str): Fields to return in the response.
        """
        self.base_url = 'https://api.semanticscholar.org/graph/v1'
        self.fields = fields

    @beartype
    def get_paper(self, paper_id: str) -> dict:
        """Get a paper by its ID.

        Args:
            paper_id (str): The ID of the paper.

        Returns:
            dict: Paper object with requested fields.
        """
        time.sleep(WAIT_SECS)

        url = '{0}/paper/{1}'.format(self.base_url, paper_id)
        response = requests.get(url, params={'fields': self.fields})
        return response.json()

    @beartype
    def get_citations(self, paper_id: str) -> list:
        """Get citations of a paper.

        Args:
            paper_id (str): The ID of the paper.

        Returns:
            list: List of citations.
        """
        time.sleep(WAIT_SECS)

        url = '{0}/paper/{1}/citations'.format(self.base_url, paper_id)
        response = requests.get(url, params={'fields': self.fields})

        if response.status_code != http.HTTPStatus.OK:
            console.log('Error: {0}'.format(response.json()), style='red')
            return []

        papers = response.json()['data']
        return [paper['citingPaper'] for paper in papers]

    @beartype
    def get_references(self, paper_id: str) -> list:
        """Get references of a paper.

        Args:
            paper_id (str): The ID of the paper.

        Returns:
            list: List of references.
        """
        time.sleep(WAIT_SECS)

        url = '{0}/paper/{1}/references'.format(self.base_url, paper_id)
        response = requests.get(url, params={'fields': self.fields})

        if response.status_code != http.HTTPStatus.OK:
            console.log('Error: {0}'.format(response.json()), style='red')
            return []

        papers = response.json()['data']
        return [paper['citedPaper'] for paper in papers]
