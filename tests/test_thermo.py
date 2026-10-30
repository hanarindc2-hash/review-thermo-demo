"""리뷰 온도 규칙 단위 테스트."""

import pytest

from app.thermo import is_mismatch, to_label, to_temperature

LABEL_CASES = [
    pytest.param(0.9, "positive", id="0.9"),
    pytest.param(0.8732, "positive", id="0.8732"),
    pytest.param(0.5, "positive", id="0.5_boundary"),
    pytest.param(0.4999, "negative", id="0.4999"),
    pytest.param(0.2, "negative", id="0.2"),
    pytest.param(0.1, "negative", id="0.1"),
]


@pytest.mark.parametrize("score, expected", LABEL_CASES)
def test_to_label(score: float, expected: str) -> None:
    assert to_label(score) == expected


TEMPERATURE_CASES = [
    pytest.param(0.0, 0.0, id="0.0"),
    pytest.param(0.2, 20.0, id="0.2"),
    pytest.param(0.4, 40.0, id="0.4"),
    pytest.param(0.5, 50.0, id="0.5"),
    pytest.param(0.8, 80.0, id="0.8"),
    pytest.param(0.8732, 87.3, id="0.8732"),
    pytest.param(1.0, 100.0, id="1.0"),
]


@pytest.mark.parametrize("score, expected", TEMPERATURE_CASES)
def test_to_temperature(score: float, expected: float) -> None:
    assert to_temperature(score) == expected


MISMATCH_CASES = [
    pytest.param(5, "positive", False, id="5_positive"),
    pytest.param(4, "positive", False, id="4_positive"),
    pytest.param(5, "negative", True, id="5_negative"),
    pytest.param(4, "negative", True, id="4_negative"),
    pytest.param(3, "positive", False, id="3_positive"),
    pytest.param(3, "negative", False, id="3_negative"),
    pytest.param(2, "positive", True, id="2_positive"),
    pytest.param(1, "positive", True, id="1_positive"),
    pytest.param(2, "negative", False, id="2_negative"),
    pytest.param(1, "negative", False, id="1_negative"),
]


@pytest.mark.parametrize("rating, label, expected", MISMATCH_CASES)
def test_is_mismatch(rating: int, label: str, expected: bool) -> None:
    assert is_mismatch(rating, label) is expected
