"""Collector main module."""

from pathlib import Path

from collector.console import console
from collector.finder import Finder


def main():
    """Run main function."""
    seeds = [
        '10.18653/v1/2021.findings-acl.353',
        '10.18653/v1/D19-1627',
        '10.18653/v1/D19-1357',
        '10.24963/ijcai.2021/520',
    ]
    year = 2015
    keywords = ['definition']
    depth = 2

    fin = Finder(seeds=seeds)
    fin.init()

    for it in range(depth):
        console.log('Collection step {0}'.format(it + 1))
        fin.collect()
        fin.filter_year(year=year)
        fin.filter_keywords(keywords=keywords)
        fin.filter_duplicates()
        fin.save_papers(Path.cwd() / 'output' / 'papers.json')

    fin.save_papers(Path.cwd() / 'output' / 'papers.json')
    console.log('Total papers: {0}'.format(len(fin.papers)))


if __name__ == '__main__':
    main()
