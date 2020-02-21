import pytest

from ..names import simplify_fore_name, simplify_last_name


@pytest.mark.parametrize(
    ("fore_name", "expected"),
    [
        (" Daniel ", "Daniel"),
        ("AB Chow", "Chow"),
        ("A.B. Chow", "Chow"),
        ("Mc-Winters", "Mc-Winters"),
        ("LE", None),
        ("Le", "Le"),
        (None, None),
        ("", None),
        (" ", None),
        ("-", None),
        ("-Rafeel!", "Rafeel"),
    ],
)
def test_simplify_fore_name(fore_name, expected):
    assert simplify_fore_name(fore_name) == expected


@pytest.mark.parametrize(
    ("fore_name", "expected"),
    [
        (" Daniel ", "daniel"),
        ("Mc-Winters", "mc-winters"),
        ("LE", None),
        ("", None),
        (" ", None),
        ("-", None),
    ],
)
def test_simplify_fore_name_lower(fore_name, expected):
    assert simplify_fore_name(fore_name, lower=True) == expected


@pytest.mark.parametrize(
    ("last_name", "expected"),
    [
        (" Heavenstone .", "Heavenstone"),
        ("Heavenstone", "Heavenstone"),
        ("", None),
        (" ", None),
        (None, None),
    ],
)
def test_simplify_last_name(last_name, expected):
    assert simplify_last_name(last_name) == expected
