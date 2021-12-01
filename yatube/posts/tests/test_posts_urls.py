from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from http import HTTPStatus

from django.urls.base import reverse

from ..models import Post, Group

user = get_user_model()


class TestU(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.cl = Client()
        cls.user = user.objects.create_user(username='HasNoName')
        cls.user_non_author = user.objects.create_user(username='AnotherUser')
        cls.post = Post.objects.create(
            author=cls.user,
            text='U TEST POST ' * 10,
        )
        cls.group = Group.objects.create(
            title='UTestGroup',
            slug='UTG',
            description='UDESC',
        )
        cls.auth_cl = Client()
        cls.auth_cl.force_login(TestU.user)
        cls.non_author_cl = Client()
        cls.non_author_cl.force_login(TestU.user_non_author)

        cls.templates = {
            '/': 'posts/index.html',
            f'/group/{cls.group.slug}/': 'posts/group_list.html',
            f'/posts/{cls.post.pk}/': 'posts/post_detail.html',
            f'/profile/{cls.user.username}/': 'posts/profile.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{cls.post.pk}/edit/': 'posts/create_post.html',
        }

    def test_posts_urls_auth_user(self):

        for adress, template in self.templates.items():
            with self.subTest(adress=adress):
                response = self.auth_cl.get(adress)
                self.assertTemplateUsed(
                    response,
                    template,
                    f"There's problem in {template} with adress - {adress}"
                )

    def test_post_create_and_edit(self):

        response = self.auth_cl.get(reverse('posts:post_create'))
        self.assertEqual(
            response.reason_phrase,
            'OK',
            f'Wrong status - {response.status_code} {response.reason_phrase},'
            f'{HTTPStatus(response.status_code).description}'
        )

        response = self.auth_cl.get(
            reverse(
                'posts:post_edition',
                kwargs={'post_id': f'{self.post.pk}'}
            )
        )

        self.assertEqual(
            response.reason_phrase,
            'OK',
            f'Wrong status - {response.status_code} {response.reason_phrase},'
            f'{HTTPStatus(response.status_code).description}'
        )

    def test_404_page(self):

        response = self.auth_cl.get('/wrong_page_404/')
        self.assertEqual(
            response.reason_phrase,
            'Not Found',
            f'Wrong status - {response.status_code} {response.reason_phrase},'
            f'{HTTPStatus(response.status_code).description}'
        )

    def test_redirects_for_users(self):

        response = self.client.get(reverse('posts:post_create'))
        self.assertRedirects(
            response,
            '/auth/login/?next=/create/'
        )

        response = self.client.get(
            reverse(
                'posts:post_edition',
                kwargs={'post_id': f'{self.post.pk}'}
            )
        )
        self.assertRedirects(
            response,
            f'/auth/login/?next=/posts/{self.post.pk}/edit/'
        )

        response = self.non_author_cl.get(
            reverse(
                'posts:post_edition',
                kwargs={'post_id': f'{self.post.pk}'}
            )
        )
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': f'{self.post.pk}'}
            )
        )
