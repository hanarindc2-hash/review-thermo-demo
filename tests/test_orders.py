from warmup.orders import average_amount, get_page


def test_average_amount():
    assert average_amount([100, 200, 300]) == 200
    assert average_amount([]) == 0
    assert average_amount([50]) == 50


def test_get_page():
    orders = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert get_page(orders, 1) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert get_page(orders, 2) == []
    assert get_page(orders, 1, size=5) == [1, 2, 3, 4, 5]
