from forj.utils.math import expr


def test_expr():
    assert expr('10 > 5') is True
    assert expr('10 > 5 and 20 < 40') is True
    assert expr('{a} >= {b}', dict(a=100, b=100)) is True
    assert expr('{a} >= {b}', dict(a=200, b=400)) is False

    assert expr('1 + 1 + 1 + 1 + 1') == 5
    assert expr('10 ** 5') == 100000
    assert expr('10 - 100') == -90
    assert expr('(10 + 20 * 50 / 2) + 100') == 610

    assert expr('10% > 5%')
