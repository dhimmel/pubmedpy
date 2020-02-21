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
    text = frontmatter_dir.joinpath(f"{pmcid}.xml").read_text(encoding='utf-8-sig')
    return etree.fromstring(text)


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
pcmid_to_authors["PMC5870622"] = [
    {
        "pmcid": "PMC5870622",
        "position": 1,
        "fore_name": "Chao",
        "last_name": "Pang",
        "corresponding": 0,
        "reverse_position": 13,
    },
    {
        "pmcid": "PMC5870622",
        "position": 2,
        "fore_name": "Fleur",
        "last_name": "Kelpin",
        "corresponding": 0,
        "reverse_position": 12,
    },
    {
        "pmcid": "PMC5870622",
        "position": 3,
        "fore_name": "David",
        "last_name": "van Enckevort",
        "corresponding": 0,
        "reverse_position": 11,
    },
    {
        "pmcid": "PMC5870622",
        "position": 4,
        "fore_name": "Niina",
        "last_name": "Eklund",
        "corresponding": 0,
        "reverse_position": 10,
    },
    {
        "pmcid": "PMC5870622",
        "position": 5,
        "fore_name": "Kaisa",
        "last_name": "Silander",
        "corresponding": 0,
        "reverse_position": 9,
    },
    {
        "pmcid": "PMC5870622",
        "position": 6,
        "fore_name": "Dennis",
        "last_name": "Hendriksen",
        "corresponding": 0,
        "reverse_position": 8,
    },
    {
        "pmcid": "PMC5870622",
        "position": 7,
        "fore_name": "Mark",
        "last_name": "de Haan",
        "corresponding": 0,
        "reverse_position": 7,
    },
    {
        "pmcid": "PMC5870622",
        "position": 8,
        "fore_name": "Jonathan",
        "last_name": "Jetten",
        "corresponding": 0,
        "reverse_position": 6,
    },
    {
        "pmcid": "PMC5870622",
        "position": 9,
        "fore_name": "Tommy",
        "last_name": "de Boer",
        "corresponding": 0,
        "reverse_position": 5,
    },
    {
        "pmcid": "PMC5870622",
        "position": 10,
        "fore_name": "Bart",
        "last_name": "Charbon",
        "corresponding": 0,
        "reverse_position": 4,
    },
    {
        "pmcid": "PMC5870622",
        "position": 11,
        "fore_name": "Petr",
        "last_name": "Holub",
        "corresponding": 0,
        "reverse_position": 3,
    },
    {
        "pmcid": "PMC5870622",
        "position": 12,
        "fore_name": "Hans",
        "last_name": "Hillege",
        "corresponding": 0,
        "reverse_position": 2,
    },
    {
        "pmcid": "PMC5870622",
        "position": 13,
        "fore_name": "Morris A",
        "last_name": "Swertz",
        "corresponding": 1,
        "reverse_position": 1,
    },
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
