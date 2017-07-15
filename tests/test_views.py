from forje.utils.test import TestCase

from django.urls import reverse


class ViewsTests(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('home'))

        assert response.status_code == 200
