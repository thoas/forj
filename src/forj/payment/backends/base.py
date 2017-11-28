class Backend(object):
    def handle_user(self, user, **kwargs):
        raise NotImplementedError

    def handle_order(self, order, **kwargs):
        raise NotImplementedError
