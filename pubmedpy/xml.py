import contextlib
import importlib
import mimetypes
import os
import zipfile

from lxml import etree


_encoding_to_module = {
    'gzip': 'gzip',
    'bzip2': 'bz2',
    'xz': 'lzma',
}


def iterparse_xml(path):
    """
    First yield the ElementTree root, then yield elements from an XML file.
    """
    # Automatically detect compression
    path = os.fspath(path)
    _, encoding = mimetypes.guess_type(path)
    if encoding is None:
        opener = open
    else:
        module = _encoding_to_module[encoding]
        opener = importlib.import_module(module).open

    # Open file and yield from the element tree
    with opener(path, 'rb') as read_file:
        context = etree.iterparse(read_file, events=('start', 'end'))
        yield next(context)[1]
        yield from (elem for event, elem in context if event == 'end')


def iter_extract_elems(path, tag):
    """
    Return elements of the specified tag from XML produced by pubmedpy.eutilities.download_pubmed_ids.
    For memory-efficiency, the XML element tree root is cleared after before yielding the next element.
    """
    path = str(path)
    parser = iterparse_xml(path)
    root = next(parser)
    for elem in parser:
        if elem.tag != tag:
            continue
        yield elem
        root.clear()
    root.clear()


def yield_etrees_from_zip(path):
    """
    Read members of a zip file with an `.xml` extension.
    """
    with zipfile.ZipFile(path) as zip_file:
        for name in zip_file.namelist():
            if not name.endswith('.xml'):
                continue
            with zip_file.open(name) as read_file:
                element_tree = etree.parse(read_file)
                yield name, element_tree
