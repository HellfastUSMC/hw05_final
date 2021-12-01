from django.test import TestCase, Client
from django.urls import reverse
from django import forms
from django.contrib.auth import get_user_model

user = get_user_model()


class TestV(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = user.objects.create_user(username='VUser')

    def test_users_views(self):

        self.auth_cl = Client()
        self.auth_cl.force_login(TestV.user)

        templates = {
            'users:signup': 'users/signup.html',
            'users:password_change_form': 'users/password_change_form.html',
            'users:password_change_done': 'users/password_change_done.html',
            'users:password_reset_form': 'users/password_reset_form.html',
            'users:password_reset_done': 'users/password_reset_done.html',
            'users:password_reset_complete':
                'users/password_reset_complete.html',
            'users:logout': 'users/logged_out.html',
        }

        users_form_fields = {
            'username': forms.CharField,
            'first_name': forms.CharField,
            'last_name': forms.CharField,
            'email': forms.CharField,
        }

        response = self.auth_cl.get(reverse('users:signup'))
        for field, f_type in users_form_fields.items():
            with self.subTest(field=field):
                self.assertIsInstance(
                    response.context['form'].fields.get(field),
                    f_type
                )

        for reverse_name, template in templates.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.auth_cl.get(reverse(reverse_name))
                self.assertTemplateUsed(response, template)
