import string

import pandas


def simplify_fore_name(name, lower=False):
    """
    # Convert period to space
    # Split on whitespace
    # Strip punctuation (on termini)
    # Discard <=1 letter strings
    # Discard <=3 letter strings that are ALL CAPS
    # If one string remains, return
    """
    if pandas.isna(name):
        return None
    assert isinstance(name, str)
    name_ = name.replace('.', ' ')
    words = name_.split()
    for word in words:
        word = word.strip(string.punctuation)
        if len(word) <= 1:
            continue
        if word.upper() == word and len(word) <= 3:
            continue
        if lower:
            word = word.lower()
        return word


import pytest


@pytest.mark.parametrize(('fore_name', 'expected'), [
    (' Daniel ', 'Daniel'),
    ('AB Chow', 'Chow'),
    ('A.B. Chow', 'Chow'),
    ('Mc-Winters', 'Mc-Winters'),
    ('LE', None),
    ('Le', 'Le'),
    (None, None),
    ('', None),
    (' ', None),
    ('-', None),
    ('-Rafeel!', 'Rafeel'),
])
def test_simplify_fore_name(fore_name, expected):
    assert simplify_fore_name(fore_name) == expected


@pytest.mark.parametrize(('fore_name', 'expected'), [
    (' Daniel ', 'daniel'),
    ('Mc-Winters', 'mc-Winters'),
    ('LE', None),
    ('', None),
    (' ', None),
    ('-', None),
])
def test_simplify_fore_name_lower(fore_name, expected):
    assert simplify_fore_name(fore_name, lower=True) == expected
