import collections
import typing

import lxml.etree


def extract_all(elem: lxml.etree._Element) -> dict:
    """
    Extract a dictionary of all supported fields from a <PubmedArticle> XML element
    """
    result = collections.OrderedDict()
    result.update(extract_identifiers(elem))
    result["journal"] = elem.findtext("MedlineCitation/MedlineJournalInfo/MedlineTA")
    result["journal_nlm_id"] = elem.findtext(
        "MedlineCitation/MedlineJournalInfo/NlmUniqueID"
    )
    result["title"] = elem.findtext("MedlineCitation/Article/ArticleTitle")
    result["publication_date"] = extract_publication_date(elem)
    result["authors"] = extract_authors(elem)
    return result


def extract_identifiers(elem: lxml.etree._Element) -> dict:
    """
    Exctract a dictionary of identifiers from a <PubmedArticle> XML element
    """
    identifiers = dict()
    renamer = {
        "pubmed": "pmid",
        "pmc": "pmcid",
        "doi": "doi",
    }
    for id_type, id_type_name in renamer.items():
        identifiers[id_type_name] = elem.findtext(
            f"PubmedData/ArticleIdList/ArticleId[@IdType={id_type!r}]"
        )
    if identifiers["doi"]:
        # convert DOIs to all lowercase for standardization
        identifiers["doi"] = identifiers["doi"].lower()
    return identifiers


def extract_publication_date(elem: lxml.etree._Element) -> typing.Optional[str]:
    """
    Select the publication date from a <PubmedArticle> XML element
    """
    dates = [
        _date_elem_to_str(x)
        for x in elem.findall("MedlineCitation/Article/ArticleDate")
    ]
    if dates:
        return sorted(dates)[0]
    else:
        pubdate = elem.find("MedlineCitation/Article/Journal/JournalIssue/PubDate")
        return _date_elem_to_str(pubdate)


_month_abbrev_to_int = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}


def _date_elem_to_str(elem: lxml.etree._Element) -> typing.Optional[str]:
    """
    Convert an XML date object to a string like '2002', '2002-01', or '2002-01-05'.
    """
    if elem is None:
        return None
    year = elem.findtext("Year")
    try:
        year = int(year)
    except (ValueError, TypeError):
        return None
    month = elem.findtext("Month")
    month = _month_abbrev_to_int.get(month, month)
    try:
        month = int(month)
    except (ValueError, TypeError):
        return f"{year:04d}"
    day = elem.findtext("Day")
    try:
        day = int(day)
    except (ValueError, TypeError):
        return f"{year:04d}-{month:02d}"
    return f"{year:04d}-{month:02d}-{day:02d}"


def extract_authors(elem: lxml.etree._Element) -> list:
    """
    Exctract a list of authors from a <PubmedArticle> XML element
    """
    authors = list()
    author_elems = elem.findall("MedlineCitation/Article/AuthorList/Author")
    for author_elem in author_elems:
        authors.append(
            {
                "fore_name": author_elem.findtext("ForeName"),
                "last_name": author_elem.findtext("LastName"),
                "affiliations": [
                    x.text for x in author_elem.findall("AffiliationInfo/Affiliation")
                ],
            }
        )
    return authors
