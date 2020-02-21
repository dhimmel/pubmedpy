import pathlib

import pytest

from ..pmc_oai import get_sets_for_pmcid, extract_authors_from_article


directory = pathlib.Path(__file__).parent


def test_get_sets_for_pmcid():
    set_specs = get_sets_for_pmcid("PMC2092437")
    assert "bmcbioi" in set_specs
    assert "pmc-open" in set_specs
