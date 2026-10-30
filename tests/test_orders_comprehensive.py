import pytest

from warmup.orders import add_tag, average_amount, get_page


@pytest.mark.parametrize(
    ("amounts", "expected"),
    [
        ([100, 200, 300], 200),
        ([], 0),
        ([50], 50),
        ([1.5, 2.5], 2.0),
        ([-10, 10], 0),
    ],
)
def test_average_amount_returns_expected_mean(amounts, expected):
    assert average_amount(amounts) == expected


def test_average_amount_rejects_non_numeric_values():
    with pytest.raises(TypeError):
        average_amount([100, "invalid"])


def test_add_tag_appends_to_supplied_tags_and_returns_order():
    order = {"id": 1}
    tags = ["priority"]

    result = add_tag(order, "gift", tags)

    assert result is order
    assert order["tags"] == ["priority", "gift"]
    assert order["tags"] is tags


def test_add_tag_uses_independent_tags_for_each_order_by_default():
    first_order = {"id": 1}
    second_order = {"id": 2}

    add_tag(first_order, "first")
    add_tag(second_order, "second")

    assert first_order["tags"] == ["first"]
    assert second_order["tags"] == ["second"]
    assert first_order["tags"] is not second_order["tags"]


def test_add_tag_rejects_an_order_that_cannot_store_tags():
    with pytest.raises(TypeError):
        add_tag([], "priority")


@pytest.mark.parametrize(
    ("orders", "page", "size", "expected"),
    [
        (list(range(1, 11)), 1, 10, list(range(1, 11))),
        (list(range(1, 11)), 2, 10, []),
        (list(range(1, 11)), 1, 5, [1, 2, 3, 4, 5]),
        (list(range(1, 11)), 2, 5, [6, 7, 8, 9, 10]),
        (list(range(1, 8)), 2, 5, [6, 7]),
        ([], 1, 10, []),
        ([42], 1, 10, [42]),
        (list(range(1, 11)), 3, 5, []),
    ],
)
def test_get_page_returns_requested_slice(orders, page, size, expected):
    assert get_page(orders, page, size) == expected


def test_get_page_rejects_a_non_numeric_page():
    with pytest.raises(TypeError):
        get_page([1, 2, 3], None)
