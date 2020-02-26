import pathlib

from lxml import etree
import requests
import pytest

from ..pmc_oai import get_sets_for_pmcid, extract_authors_from_article


directory = pathlib.Path(__file__).parent


def test_get_sets_for_pmcid():
    set_specs = get_sets_for_pmcid("PMC2092437")
    assert "bmcbioi" in set_specs
    assert "pmc-open" in set_specs


def get_frontmatter_etree(pmcid):
    frontmatter_dir = directory.joinpath("data", "pmc-frontmatter")
    text = frontmatter_dir.joinpath(f"{pmcid}.xml").read_text(encoding="utf-8-sig")
    return etree.fromstring(text)


def get_frontmatter_etree_via_api(pmcid):
    url = f"https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:{pmcid[3:]}&metadataPrefix=pmc_fm"
    response = requests.get(url)
    tree = etree.fromstring(response.content)
    article = tree.find("{*}GetRecord/{*}record/{*}metadata/{*}article")
    return article


pcmid_to_authors = dict()
pcmid_to_authors["PMC65048"] = [
    {
        "pmcid": "PMC65048",
        "position": 1,
        "fore_name": "Kevin",
        "last_name": "Truong",
        "corresponding": 0,
        "reverse_position": 2,
        "affiliations": [
            "1 Division of Molecular and Structural Biology, Ontario Cancer Institute and Department of Medical Biophysics, University of Toronto, Toronto, Ontario, Canada"
        ],
    },
    {
        "pmcid": "PMC65048",
        "position": 2,
        "fore_name": "Mitsuhiko",
        "last_name": "Ikura",
        "corresponding": 1,
        "reverse_position": 1,
        "affiliations": [
            "1 Division of Molecular and Structural Biology, Ontario Cancer Institute and Department of Medical Biophysics, University of Toronto, Toronto, Ontario, Canada"
        ],
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
        "affiliations": [
            "Bioinformatics Program, Boston University, Boston, Massachusetts, United States of America"
        ],
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
        "affiliations": [
            "1 Department of Genetics, Genomics Coordination Center, University Medical Center Groningen, University of Groningen, Groningen, The Netherlands",
            "2 Department of Epidemiology, University Medical Center Groningen, University of Groningen, Groningen, The Netherlands",
        ],
    },
    {
        "pmcid": "PMC5870622",
        "position": 2,
        "fore_name": "Fleur",
        "last_name": "Kelpin",
        "corresponding": 0,
        "reverse_position": 12,
        "affiliations": [
            "1 Department of Genetics, Genomics Coordination Center, University Medical Center Groningen, University of Groningen, Groningen, The Netherlands"
        ],
    },
    {
        "pmcid": "PMC5870622",
        "position": 3,
        "fore_name": "David",
        "last_name": "van Enckevort",
        "corresponding": 0,
        "reverse_position": 11,
        "affiliations": [
            "1 Department of Genetics, Genomics Coordination Center, University Medical Center Groningen, University of Groningen, Groningen, The Netherlands"
        ],
    },
    {
        "pmcid": "PMC5870622",
        "position": 4,
        "fore_name": "Niina",
        "last_name": "Eklund",
        "corresponding": 0,
        "reverse_position": 10,
        "affiliations": [
            "3 Department of Public Health Solutions, National Institute for Health and Welfare, Helsinki, Finland"
        ],
    },
    {
        "pmcid": "PMC5870622",
        "position": 5,
        "fore_name": "Kaisa",
        "last_name": "Silander",
        "corresponding": 0,
        "reverse_position": 9,
        "affiliations": [
            "3 Department of Public Health Solutions, National Institute for Health and Welfare, Helsinki, Finland"
        ],
    },
    {
        "pmcid": "PMC5870622",
        "position": 6,
        "fore_name": "Dennis",
        "last_name": "Hendriksen",
        "corresponding": 0,
        "reverse_position": 8,
        "affiliations": [
            "1 Department of Genetics, Genomics Coordination Center, University Medical Center Groningen, University of Groningen, Groningen, The Netherlands"
        ],
    },
    {
        "pmcid": "PMC5870622",
        "position": 7,
        "fore_name": "Mark",
        "last_name": "de Haan",
        "corresponding": 0,
        "reverse_position": 7,
        "affiliations": [
            "1 Department of Genetics, Genomics Coordination Center, University Medical Center Groningen, University of Groningen, Groningen, The Netherlands"
        ],
    },
    {
        "pmcid": "PMC5870622",
        "position": 8,
        "fore_name": "Jonathan",
        "last_name": "Jetten",
        "corresponding": 0,
        "reverse_position": 6,
        "affiliations": [
            "1 Department of Genetics, Genomics Coordination Center, University Medical Center Groningen, University of Groningen, Groningen, The Netherlands"
        ],
    },
    {
        "pmcid": "PMC5870622",
        "position": 9,
        "fore_name": "Tommy",
        "last_name": "de Boer",
        "corresponding": 0,
        "reverse_position": 5,
        "affiliations": [
            "1 Department of Genetics, Genomics Coordination Center, University Medical Center Groningen, University of Groningen, Groningen, The Netherlands"
        ],
    },
    {
        "pmcid": "PMC5870622",
        "position": 10,
        "fore_name": "Bart",
        "last_name": "Charbon",
        "corresponding": 0,
        "reverse_position": 4,
        "affiliations": [
            "1 Department of Genetics, Genomics Coordination Center, University Medical Center Groningen, University of Groningen, Groningen, The Netherlands"
        ],
    },
    {
        "pmcid": "PMC5870622",
        "position": 11,
        "fore_name": "Petr",
        "last_name": "Holub",
        "corresponding": 0,
        "reverse_position": 3,
        "affiliations": [
            "4 Biobanking and BioMolecular Resources Research Infrastructure (BBMRI-ERIC), Graz, Austria"
        ],
    },
    {
        "pmcid": "PMC5870622",
        "position": 12,
        "fore_name": "Hans",
        "last_name": "Hillege",
        "corresponding": 0,
        "reverse_position": 2,
        "affiliations": [
            "2 Department of Epidemiology, University Medical Center Groningen, University of Groningen, Groningen, The Netherlands"
        ],
    },
    {
        "pmcid": "PMC5870622",
        "position": 13,
        "fore_name": "Morris A",
        "last_name": "Swertz",
        "corresponding": 1,
        "reverse_position": 1,
        "affiliations": [
            "1 Department of Genetics, Genomics Coordination Center, University Medical Center Groningen, University of Groningen, Groningen, The Netherlands",
            "2 Department of Epidemiology, University Medical Center Groningen, University of Groningen, Groningen, The Netherlands",
        ],
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
    """
    NOTE: PMC2373917 is an example of where affiliations are encoded in a non-semantic way.
    https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:2373917&metadataPrefix=pmc_fm
    """
    article = get_frontmatter_etree(pmcid)
    authors = extract_authors_from_article(article)
    print(authors)
    assert authors == expected


def test_extract_authors_from_article_PMC3003546():
    """
    aff is a child of contrib-group rather than article-meta for PMC3003546
    https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:3003546&metadataPrefix=pmc_fm
    """
    pmcid = "PMC3003546"
    article = get_frontmatter_etree_via_api(pmcid)
    authors = extract_authors_from_article(article)
    assert "University of California San Diego" in authors[0]["affiliations"][0]


def test_extract_authors_from_article_PMC4372613():
    """
    Affiliation name is under <aff><addr-line> for PMC4372613.
    https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:4372613&metadataPrefix=pmc_fm
    """
    pmcid = "PMC4372613"
    article = get_frontmatter_etree_via_api(pmcid)
    authors = extract_authors_from_article(article)
    assert "California Institute of Technology" in authors[0]["affiliations"][0]
