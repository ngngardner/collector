"""Use PyPaperBot to download papers."""

import json
import subprocess
from pathlib import Path

from rich.console import Console

DEFAULT_PATH = Path.cwd() / 'output'
INPUT_FILE = DEFAULT_PATH / 'papers.json'
DOI_TXT = DEFAULT_PATH / 'doi.txt'
PDF_DIR = DEFAULT_PATH / 'papers'

console = Console()


class Downloader(object):
    """Download papers."""

    def __init__(
        self,
        input_file: Path = INPUT_FILE,
        doi_txt: Path = DOI_TXT,
        pdf_dir: Path = PDF_DIR,
    ):
        """Initialize.

        Args:
            input_file (Path): Path to input file.
            doi_txt (Path): Path to output file.
            pdf_dir (Path): Path to output directory.
        """
        self.input_file = input_file
        self.doi_txt = doi_txt
        self.pdf_dir = pdf_dir

        # create directories
        self.doi_txt.parent.mkdir(parents=True, exist_ok=True)
        self.pdf_dir.mkdir(parents=True, exist_ok=True)

    def convert(self):
        """Convert json input_file to txt file to be read by PyPaperBot."""
        console.log('Converting {0} to {1}'.format(
            self.input_file,
            self.doi_txt,
        ))

        with open(self.input_file, 'r') as fin:
            papers = json.load(fin)

        with open(self.doi_txt, 'w') as fout:
            for paper in papers:
                try:
                    doi = paper['externalIds']['DOI']
                except Exception:
                    console.log(
                        'No DOI for "{0}".'.format(paper['title']),
                        style='yellow',
                    )
                    continue
                fout.write('{0}\n'.format(doi))

    def download(self):
        """Call PyPaperBot on doi_txt."""
        console.log('Downloading papers from {0}'.format(self.doi_txt))

        subprocess.run(
            [
                'PyPaperBot',
                '--doi-file',
                str(self.doi_txt),
                '--dwn-dir',
                str(self.pdf_dir),
                # only download pdfs, not bibtex
                '--restrict',
                '1',
            ],
            check=True,
        )


if __name__ == '__main__':
    downloader = Downloader()
    downloader.convert()
    downloader.download()
