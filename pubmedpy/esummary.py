import collections
import contextlib
import datetime
import itertools
import locale
import logging
import re
import threading
from typing import List, Optional

import pandas
import tqdm
import lxml.etree

from .xml import iter_extract_elems
from .utils import PathType

locale_lock = threading.Lock()


@contextlib.contextmanager
def setlocale(name: str):
    """
    Context manager to temporarily set locale for datetime.datetime.strptime
    https://stackoverflow.com/a/24070673/4651668
    """
    with locale_lock:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)


def parse_date_text(text: str) -> datetime.date:
    """
    Parse an `eSummaryResult/DocSum/Item[@Name='History']/Item[@Type='Date']`
    element.
    The time on the date is discarded. A `datetime.date` object is returned
    """
    with setlocale("C"):
        return datetime.datetime.strptime(text, "%Y/%m/%d %H:%M").date()


def parse_pubdate_text(text: str) -> datetime.date:
    """
    Parse the text contained by the following elements:

    `eSummaryResult/DocSum/Item[@Name='PubDate' @Type='Date']`
    `eSummaryResult/DocSum/Item[@Name='EPubDate' @Type='Date']`

    See https://www.nlm.nih.gov/bsd/licensee/elements_article_source.html
    A `datetime.date` object is returned.
    """
    return datetime.datetime.strptime(text, "%Y %b %d").date()


def parse_esummary_history(docsum: lxml.etree._Element) -> dict:
    """
    docsum is an xml Element.
    """
    # Extract all historical dates
    date_pairs = list()
    seen = set()
    for item in docsum.findall("Item[@Name='History']/Item[@Type='Date']"):
        name = item.get("Name")
        try:
            date_ = parse_date_text(item.text)
        except ValueError as e:
            id_ = int(docsum.findtext("Id"))
            msg = f"article {id_}; name: {name}; " f"date: {item.text}; error: {e}"
            logging.warning(msg)
            continue

        date_pair = name, date_
        if date_pair in seen:
            continue
        seen.add(date_pair)
        date_pairs.append(date_pair)
    date_pairs.sort(key=lambda x: x[0])
    history = collections.OrderedDict()
    for name, group in itertools.groupby(date_pairs, key=lambda x: x[0]):
        for i, (name, date_) in enumerate(group):
            history[f"{name}_{i}"] = date_
    return history


def parse_esummary_pubdates(docsum: lxml.etree._Element) -> dict:
    """
    Parse PubDate and EPubDate. Infer first published date.
    """
    pubdates = collections.OrderedDict()
    for key, name in ("pub", "PubDate"), ("epub", "EPubDate"):
        xpath = f"Item[@Name='{name}'][@Type='Date']"
        text = docsum.findtext(xpath)
        try:
            pubdates[key] = parse_pubdate_text(text)
        except ValueError as e:
            id_ = int(docsum.findtext("Id"))
            msg = f"article {id_}; name: {key}; " f"date: {text}; error: {e}"
            logging.info(msg)
            continue
    dates = set(pubdates.values())
    dates.discard(None)
    if dates:
        pubdates["published"] = min(dates)
    return pubdates


def parse_esummary_article_info(elem: lxml.etree._Element) -> dict:
    """
    Extract general article information
    """
    article = collections.OrderedDict()
    article["pubmed_id"] = int(elem.findtext("Id"))
    article["journal_nlm_id"] = elem.findtext("Item[@Name='NlmUniqueID']")
    article["journal"] = elem.findtext("Item[@Name='Source']")
    article["title"] = elem.findtext("Item[@Name='Title']")
    article["doi"] = elem.findtext("Item[@Name='DOI']")
    # https://www.ncbi.nlm.nih.gov/books/NBK3827/table/pubmedhelp.T.publication_types/
    article["publication_types"] = " | ".join(
        x.text for x in elem.findall("Item[@Name='PubTypeList']/Item[@Name='PubType']")
    )
    # get incoming citation count. https://github.com/dhimmel/pubmedpy/issues/2
    pmc_cited_by_count = elem.findtext("Item[@Name='PmcRefCount']")
    try:
        pmc_cited_by_count = int(pmc_cited_by_count)
    except (TypeError, ValueError):
        pmc_cited_by_count = None
    article["pmc_cited_by_count"] = pmc_cited_by_count
    return article


def parse_esummary(elem: lxml.etree._Element) -> dict:
    """
    Extract pubmed, journal, and date information from an eSummaryResult/DocSum
    """
    article = parse_esummary_article_info(elem)
    article.update(parse_esummary_pubdates(elem))
    article.update(parse_esummary_history(elem))
    return article


def extract_articles_from_esummaries(
    path: PathType, n_articles: Optional[int] = None, tqdm=tqdm.tqdm
) -> List[dict]:
    """
    Extract a list of articles (dictionaries with date information) from a
    an eSummaryResult XML file. Specify `n_articles` to enable a progress bar.
    """
    if n_articles is not None:
        progress_bar = tqdm(total=n_articles, unit="articles")

    articles = list()
    for elem in iter_extract_elems(path, tag="DocSum"):
        article = parse_esummary(elem)
        articles.append(article)
        if n_articles is not None:
            progress_bar.update(1)

    if n_articles is not None:
        progress_bar.close()
    return articles


def articles_to_dataframe(articles: List[dict]) -> pandas.DataFrame:
    """
    Convert a list of articles created by `extract_articles_from_esummaries`
    into a pandas.DataFrame.
    """
    article_df = pandas.DataFrame(articles)
    article_df = article_df.sort_values(by="pubmed_id")
    # Enforce a consistent column ordering
    columns = article_df.columns[2:].tolist()
    columns = [
        "pubmed_id",
        "journal_nlm_id",
        "journal",
        "doi",
        *sorted(x for x in columns if re.search("pub(?!med)", x)),
        *sorted(x for x in columns if re.search("_[0-9]+$", x)),
        "title",
        "pmc_cited_by_count",
    ]
    article_df = article_df[columns]
    return article_df
