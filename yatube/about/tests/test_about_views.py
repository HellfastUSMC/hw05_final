from django.test import TestCase, Client
from django.urls import reverse

anon_cl = Client()


class TestU(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.cl = Client()

    def test_about_urls(self):

        templates = {
            reverse('about:tech'): 'about/tech.html',
            reverse('about:author'): 'about/author.html',
        }

        for reverse_name, template in templates.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.cl.get(reverse_name)
                self.assertTemplateUsed(response, template)
