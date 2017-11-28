class DummyBackend(object):
    def handle_user(self, user, **kwargs):
        return user

    def handle_order(self, order, **kwargs):
        return order
