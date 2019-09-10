import time
import collections
import logging

import requests
import lxml.etree
import tqdm


def esearch_query(payload, retmax=10000, sleep=0.34, tqdm=tqdm.tqdm):
    """
    Return identifiers using the ESearch E-utility.

    Set `tqdm=tqdm.notebook` to use the tqdm notebook interface.
    """
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    payload['rettype'] = 'xml'
    payload['retmax'] = retmax
    payload['retstart'] = 0
    ids = list()
    count = 1
    progress_bar = None
    while payload['retstart'] < count:
        response = requests.get(url, params=payload)
        tree = lxml.etree.fromstring(response.content)
        count = int(tree.findtext('Count'))
        if not progress_bar:
            progress_bar = tqdm(total=count, unit='ids')
        add_ids = [id_.text for id_ in tree.findall('IdList/Id')]
        ids += add_ids
        payload['retstart'] += retmax
        progress_bar.update(len(add_ids))
        time.sleep(sleep)
    progress_bar.close()
    return ids


def download_pubmed_ids(
        ids, write_file, endpoint='esummary', retmax=100, retmin=20, sleep=0.34,
        error_sleep=10, tqdm=tqdm.tqdm):
    """
    Submit an ESummary or EFetch query for PubMed records and write results as xml
    to write_file.

    Set `tqdm=tqdm.notebook` to use the tqdm notebook interface.
    """
    # Base URL for PubMed's esummary eutlity
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/{endpoint}.fcgi'

    # Set up progress stats
    n_total = len(ids)
    successive_errors = 0
    progress_bar = tqdm(total=n_total, unit='articles')
    initialize_xml = True

    # Set up queue
    idq = collections.deque()
    for i in range(0, len(ids), retmax):
        idq.append(ids[i:i + retmax])

    # Query until the queue is empty
    while idq:
        time.sleep(sleep)
        id_subset = idq.popleft()
        id_subset_len = len(id_subset)

        # Perform eutilities API request
        id_string = ','.join(map(str, id_subset))
        payload = {'db': 'pubmed', 'id': id_string, 'rettype': 'xml'}
        try:
            response = requests.get(url, params=payload)
            response.raise_for_status()
            tree = lxml.etree.fromstring(response.content)
            successive_errors = 0
        except Exception as e:
            successive_errors += 1
            logging.warning(
                f'{successive_errors} successive error: {id_subset_len} IDs'
                f'[{id_subset[0]} … {id_subset[-1]}] threw {e}'
            )
            if id_subset_len >= retmin * 2:
                mid = len(id_subset) // 2
                idq.appendleft(id_subset[:mid])
                idq.appendleft(id_subset[mid:])
            else:
                idq.appendleft(id_subset)
            time.sleep(error_sleep * successive_errors)
            continue

        # Write XML to file
        if initialize_xml:
            initialize_xml = False
            write_file.write(f'<{tree.tag}>\n')
        for elem in tree.getchildren():
            xml_str = lxml.etree.tostring(elem, encoding='unicode')
            write_file.write(xml_str.rstrip() + '\n')

        # Report progress
        progress_bar.update(id_subset_len)

    progress_bar.close()
    # Write final line of XML
    write_file.write(f'</{tree.tag}>\n')
