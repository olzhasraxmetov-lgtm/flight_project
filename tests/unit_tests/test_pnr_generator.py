import re

from app.utils.pnr_generator import generate_pnr_identifier


def test_pnr_generator_valid():
    length = 6
    res = generate_pnr_identifier(length)
    assert isinstance(res, str)
    assert len(res) == length
    assert res.isalnum()
    assert re.match(r"^[A-Z0-9]+$", res)