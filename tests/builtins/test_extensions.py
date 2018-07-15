from django.template import engines


def test_amountformat():
    engine = engines["backend"]

    template = engine.from_string("{{ amount|amountformat(-2) }}")
    content = template.render({"amount": 360})

    assert content == "3,60"

    content = template.render({"amount": 300})

    assert content == "3"
