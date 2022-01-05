"""Use bibtex file to generate list of doi numbers."""

from pathlib import Path

import bibtexparser

from rich.console import Console

DEFAULT_PATH = Path.cwd() / 'output'
INPUT_FILE = DEFAULT_PATH / 'input.bib'
OUTPUT_FILE = DEFAULT_PATH / 'doi.txt'

console = Console()

if __name__ == '__main__':
    with INPUT_FILE.open() as fin:
        bib_database = bibtexparser.load(fin)

    with OUTPUT_FILE.open('w') as fout:
        for entry in bib_database.entries:
            doi = entry.get('doi', None)
            if doi:
                fout.write('{0} \n'.format(doi))

    console.print('Wrote {0}'.format(OUTPUT_FILE))
