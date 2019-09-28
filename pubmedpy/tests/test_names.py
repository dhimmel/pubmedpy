import pytest

from ..names import simplify_fore_name


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
