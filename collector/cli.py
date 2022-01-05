"""Functionality for the command line interface."""
import questionary
from beartype import beartype

from collector import const
from collector.console import console
from collector.finder import Finder


@beartype
def get_seeds() -> list[str]:
    """Get the seed papers.

    Returns:
        list[str]: The seed papers as a list of DOI strings.

    Raises:
        ValueError: If no seed papers are specified.
    """
    seeds = []

    res = questionary.text('Enter DOI of a seed paper to get started.').ask()

    console.log('You may provide additional seed papers.')
    while res != '':
        seeds.append(res)
        res = questionary.text(
            'Enter additional papers by DOI. Press enter to skip.',
        ).ask()

    if not seeds:
        raise ValueError('No seed papers provided.')

    return seeds


@beartype
def get_keywords() -> list[str]:
    """Get the keywords to filter papers by.

    Returns:
        list[str]: The keywords as a list of strings.

    Raises:
        ValueError: If no keywords are specified.
    """
    keywords = []

    console.log('Keywords will be used to filter papers.')
    console.log('For a paper to be selected, each keyword (logic AND) must be')
    console.log('present in the title or abstract of the paper.')

    res = questionary.text('Enter keywords to filter papers by.').ask()

    console.log('You may provide additional keywords.')
    while res != '':
        keywords.append(res)
        res = questionary.text(
            'Enter additional keywords. Press enter to skip.',
        ).ask()

    if not keywords:
        raise ValueError('No keywords provided.')

    return keywords


@beartype
def get_year() -> int:
    """Get the year to filter by.

    Returns:
        int: The year to filter by.
    """
    console.log('A year can be given to filter papers. If provided, papers')
    console.log('with a year before the given year will be filtered out.')

    year = questionary.text(
        'Enter the year to filter by. Press enter to skip.',
    ).ask()

    if year == '':
        year = '0'

    return int(year)


@beartype
def get_depth() -> int:
    """Get the depth of papers to seek.

    Returns:
        int: The depth of papers to seek.
    """
    depth = questionary.text(
        'Enter the recursive depth of papers to seek. (default=1)',
    ).ask()

    if depth == '':
        depth = '1'

    return int(depth)


@beartype
def run_finder(
    seeds: list[str],
    keywords: list[str],
    year: int,
    depth: int,
):
    """Run the finder.

    Args:
        seeds: The seed papers to start the search from.
        keywords: The keywords to filter papers by.
        year: The year to filter by.
        depth: The depth of papers to seek.
    """
    console.log('Initializing finder.')
    fin = Finder(seeds=seeds)
    fin.init()

    for it in range(depth):
        console.log('Collection step {0}'.format(it + 1))
        fin.collect()

        if year:
            fin.filter_year(year=year)

        fin.filter_keywords(keywords=keywords)
        fin.filter_duplicates()
        fin.save_papers(const.OUTPUT_FILE)
    console.log('Total papers: {0}'.format(len(fin.papers)))


def cli():
    """Run main cli program."""
    console.log('This program will recusively collect papers related to the')
    console.log('seed papers you provide by recursively searching through the')
    console.log('references and citations of the collected papers.')

    seeds = get_seeds()
    keywords = get_keywords()
    year = get_year()
    depth = get_depth()

    run_finder(seeds=seeds, keywords=keywords, year=year, depth=depth)
