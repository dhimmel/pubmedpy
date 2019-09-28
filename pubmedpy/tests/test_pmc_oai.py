from ..pmc_oai import get_sets_for_pmcid


def test_get_sets_for_pmcid():
    set_specs = get_sets_for_pmcid('PMC2092437')
    assert 'bmcbioi' in set_specs
    assert 'pmc-open' in set_specs
