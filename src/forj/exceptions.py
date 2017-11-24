class ForjException(Exception):
    pass


class InvalidProductRef(ForjException):
    pass


class CardError(ForjException):
    pass


class PaymentError(ForjException):
    pass
