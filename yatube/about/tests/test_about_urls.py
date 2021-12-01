from django.test import TestCase, Client
from http import HTTPStatus

anon_cl = Client()


class TestU(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.cl = Client()

    def test_about_urls(self):

        response = self.cl.get('/about/author/')
        self.assertEqual(
            response.reason_phrase,
            'OK',
            f'Wrong status - {response.status_code} {response.reason_phrase},'
            f'{HTTPStatus(response.status_code).description}'
        )

        response = self.cl.get('/about/tech/')
        self.assertEqual(
            response.reason_phrase,
            'OK',
            f'Wrong status - {response.status_code} {response.reason_phrase},'
            f'{HTTPStatus(response.status_code).description}'
        )

        response = self.cl.get('/about/author/')
        self.assertTemplateUsed(
            response,
            'about/author.html',
            "There's problem in template!"
        )

        response = self.cl.get('/about/tech/')
        self.assertTemplateUsed(
            response,
            'about/tech.html',
            "There's problem in template!"
        )
