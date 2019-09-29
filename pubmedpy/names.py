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


def simplify_last_name(name, lower=False):
    """
    Strip punctuation and whitespace (on termini)
    """
    if pandas.isna(name):
        return None
    assert isinstance(name, str)
    name = name.strip(string.whitespace + string.punctuation)
    if not name:
        return None
    if lower:
        name = name.lower()
    return name