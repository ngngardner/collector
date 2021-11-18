"""Build ASReview dataset."""

import json
from pathlib import Path

from rich.console import Console

DEFAULT_PATH = Path.cwd() / 'output'
INPUT_FILE = DEFAULT_PATH / 'papers.json'
OUTPUT_FILE = DEFAULT_PATH / 'dataset.csv'

console = Console()


class Dataset(object):
    """Build ASReview dataset."""

    def __init__(
        self,
        input_file: Path = INPUT_FILE,
        output_file: Path = OUTPUT_FILE,
    ):
        """Initialize Dataset.

        Args:
            input_file: Path to input file.
            output_file: Path to output file.
        """
        self.input_file = input_file
        self.output_file = output_file

    def convert(self):
        """Convert to csv."""
        with open(self.input_file, 'r') as fin:
            papers = json.load(fin)

        with open(self.output_file, 'w') as fout:
            fout.write('id,title,abstract\n')
            for paper in papers:
                title = paper['title']
                abstract = paper['abstract']
                # remove commas
                title = title.replace(',', ' ')
                abstract = abstract.replace(',', ' ')
                fout.write('{0},{1},{2}\n'.format(
                    paper['paperId'],
                    title,
                    abstract,
                ))


if __name__ == '__main__':
    dataset = Dataset()
    dataset.convert()
