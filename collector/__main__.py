"""Collector main module."""

from collector.console import console
from collector.finder import Finder


def main():
    """Run main function."""
    doi = '10.1016/j.ins.2019.11.042'
    year = 2016
    keywords = ['texture', 'color', 'spectral']
    depth = 2

    fin = Finder(seed=doi)
    fin.init()

    for it in range(depth):
        console.log('Collection step {0}'.format(it + 1))
        fin.collect()
        fin.filter_year(year=year)
        fin.filter_keywords(keywords=keywords)
        fin.filter_duplicates()

    fin.save_papers('output')
    console.log('Total papers: {0}'.format(len(fin.papers)))


if __name__ == '__main__':
    main()