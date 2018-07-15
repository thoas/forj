from django.conf import settings

from mail_factory import factory, mails


class BaseMail(mails.BaseMail):
    def get_context_data(self, *args, **kwargs):
        return {
            "FORJ_CONTACT_EMAIL": settings.FORJ_CONTACT_EMAIL,
            "FORJ_PHONE_NUMBER": settings.FORJ_PHONE_NUMBER,
        }


class ConfirmationMail(BaseMail):
    template_name = "confirmation"
    params = ["order"]


factory.register(ConfirmationMail)
