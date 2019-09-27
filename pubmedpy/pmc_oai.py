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


def download_frontmatter_set(oai_set, path, tqdm=None, n_records=None):
    """
    Download an OAI set to a zipped file specified by path. Each file in the zip archive contains
    frontmatter XML for a single article from the set.
    """
    import lxml.etree
    sickler = get_sickle()
    zip_file = zipfile.ZipFile(path, mode='w', compression=zipfile.ZIP_LZMA)
    records = sickler.ListRecords(metadataPrefix="pmc_fm", set=oai_set, ignore_deleted=True)
    if tqdm is not None:
        records = tqdm(records, total=n_records, desc=oai_set)
    for record in records:
        article = record.xml.find("oai:metadata/{*}article", namespaces=namespaces)
        if article is None:
            logging.warning(f'failure to extract <article> from\n{record.raw}')
        pmcid = article.findtext("{*}front/{*}article-meta/{*}article-id[@pub-id-type='pmcid']")
        xml_str = lxml.etree.tostring(article, encoding='unicode')
        zip_file.writestr(f'{pmcid}.xml', data=xml_str)
    zip_file.close()