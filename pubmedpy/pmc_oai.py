"""
Functions for querying the PubMed Central OAI-PMH service (PMC-OAI).
More information is available at https://www.ncbi.nlm.nih.gov/pmc/tools/oai/
"""

import functools
import logging
import zipfile

# URL to the OAI endpoint for PMC
endpoint = "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi"

# Namespaces abbreviations for parsing PMC-OAI XML
namespaces = {
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "jats": "https://jats.nlm.nih.gov/ns/archiving/1.2/",
    "dtd": "https://dtd.nlm.nih.gov/ns/archiving/2.3/",
}


@functools.lru_cache()
def get_sickle():
    """
    Return a sickle OAI harvester for PMC
    """
    import sickle

    return sickle.Sickle(endpoint=endpoint)


def get_sets_for_pmcid(pmcid):
    """
    Return the OAI sets specified to include the provided PMC identifier.
    """
    pmcid = str(pmcid)
    if pmcid.upper().startswith("PMC"):
        pmcid = pmcid[3:]
    sickler = get_sickle()
    record = sickler.GetRecord(
        identifier=f"oai:pubmedcentral.nih.gov:{pmcid}", metadataPrefix="pmc_fm"
    )
    return record.header.setSpecs


def download_frontmatter_set(oai_set, path, tqdm=None, n_records=None):
    """
    Download an OAI set to a zipped file specified by path. Each file in the zip archive contains
    frontmatter XML for a single article from the set.
    """
    import lxml.etree

    sickler = get_sickle()
    zip_file = zipfile.ZipFile(path, mode="w", compression=zipfile.ZIP_LZMA)
    records = sickler.ListRecords(
        metadataPrefix="pmc_fm", set=oai_set, ignore_deleted=True
    )
    if tqdm is not None:
        records = tqdm(records, total=n_records, desc=oai_set)
    for record in records:
        article = record.xml.find("oai:metadata/{*}article", namespaces=namespaces)
        if article is None:
            logging.warning(f"failure to extract <article> from\n{record.raw}")
        pmcid = article.findtext(
            "{*}front/{*}article-meta/{*}article-id[@pub-id-type='pmcid']"
        )
        xml_str = lxml.etree.tostring(article, encoding="unicode")
        zip_file.writestr(f"{pmcid}.xml", data=xml_str)
    zip_file.close()


def _contrib_elem_is_corresp(contrib_elem):
    if contrib_elem.find("{*}xref[@ref-type='corresp']") is not None:
        return True
    return contrib_elem.get("corresp", "no") == "yes"


def _get_id_to_affiliation(article) -> dict:
    aff_elems = article.findall("{*}front/{*}article-meta//{*}aff")
    id_to_affiliation = dict()
    for elem in aff_elems:
        texts = [elem.text, *(child.tail for child in elem), elem.tail]
        affiliation = "".join(x.strip() for x in texts if x)
        id_to_affiliation[elem.get("id")] = affiliation
    return id_to_affiliation


def extract_authors_from_article(article):
    """
    Extract author information from frontmatter XML into a list of dictionaries.
    """
    pmcid = article.findtext(
        "{*}front/{*}article-meta/{*}article-id[@pub-id-type='pmcid']"
    )
    contrib_elems = article.findall(
        "{*}front/{*}article-meta/{*}contrib-group/{*}contrib[@contrib-type='author']"
    )
    id_to_affiliation = _get_id_to_affiliation(article)
    authors = []
    for i, contrib_elem in enumerate(contrib_elems):
        fore_name = contrib_elem.findtext("{*}name/{*}given-names")
        last_name = contrib_elem.findtext("{*}name/{*}surname")
        aff_ids = [
            aff.get("rid") for aff in contrib_elem.findall("{*}xref[@ref-type='aff']")
        ]
        authors.append(
            {
                "pmcid": pmcid,
                "position": i + 1,
                "fore_name": _strip_str(fore_name),
                "last_name": _strip_str(last_name),
                "corresponding": int(_contrib_elem_is_corresp(contrib_elem)),
                "reverse_position": len(contrib_elems) - i,
                "affiliations": [id_to_affiliation[aff_id] for aff_id in aff_ids],
            }
        )
    return authors


def _strip_str(value):
    """Strip whitespace if value is a string."""
    if isinstance(value, str):
        value = value.strip()
    return value
