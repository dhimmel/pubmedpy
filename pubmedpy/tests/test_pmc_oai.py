import pathlib

import pytest

from ..pmc_oai import get_sets_for_pmcid, extract_authors_from_article


directory = pathlib.Path(__file__).parent


def test_get_sets_for_pmcid():
    set_specs = get_sets_for_pmcid("PMC2092437")
    assert "bmcbioi" in set_specs
    assert "pmc-open" in set_specs


def get_frontmatter_etree(pmcid):
    from lxml import etree

    frontmatter_dir = directory.joinpath("data", "pmc-frontmatter")
    with frontmatter_dir.joinpath(f"{pmcid}.xml").open() as read_file:
        return etree.parse(read_file)


pcmid_to_authors = dict()
pcmid_to_authors["PMC65048"] = [
    {
        "pmcid": "PMC65048",
        "position": 1,
        "fore_name": "Kevin",
        "last_name": "Truong",
        "corresponding": 0,
        "reverse_position": 2,
    },
    {
        "pmcid": "PMC65048",
        "position": 2,
        "fore_name": "Mitsuhiko",
        "last_name": "Ikura",
        "corresponding": 1,
        "reverse_position": 1,
    },
]
pcmid_to_authors["PMC1183515"] = [
    {
        "pmcid": "PMC1183515",
        "position": 1,
        "fore_name": "Boris E",
        "last_name": "Shakhnovich",
        "corresponding": 1,
        "reverse_position": 1,
    }
]


@pytest.mark.parametrize(
    ["pmcid", "expected"],
    [
        pytest.param(pmcid, authors, id=pmcid)
        for pmcid, authors in pcmid_to_authors.items()
    ],
)
def test_extract_authors_from_article(pmcid, expected):
    article = get_frontmatter_etree(pmcid)
    authors = extract_authors_from_article(article)
    print(authors)
    assert authors == expected
