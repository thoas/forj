class DummyBackend(object):
    def handle_order(self, order, **kwargs):
        return order
