from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

user = get_user_model()


class TestM(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = user.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='TestGroup',
            slug='TG',
            description='DESC',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='TEST POST ' * 10,
        )
        cls.group_fields = {
            'title': cls.group.title,
            'slug': cls.group.slug,
            'description': cls.group.description,
        }
        cls.group_verbose_fields = {
            'title': cls.group._meta.get_field('title').verbose_name,
            'slug': cls.group._meta.get_field('slug').verbose_name,
            'description':
                cls.group._meta.get_field('description').verbose_name,
        }
        cls.group_help_fields = {
            'title': cls.group._meta.get_field('title').help_text,
            'slug': cls.group._meta.get_field('slug').help_text,
            'description': cls.group._meta.get_field('description').help_text,
        }

        cls.post_fields = {
            'author': cls.post.author,
            'group': cls.post.group,
            'text': cls.post.text,
            'pub_date': cls.post.pub_date,
        }
        cls.post_verbose_fields = {
            'author': cls.post._meta.get_field('author').verbose_name,
            'group': cls.post._meta.get_field('group').verbose_name,
            'text': cls.post._meta.get_field('text').verbose_name,
            'pub_date': cls.post._meta.get_field('pub_date').verbose_name,
        }
        cls.post_help_fields = {
            'author': cls.post._meta.get_field('author').help_text,
            'group': cls.post._meta.get_field('group').help_text,
            'text': cls.post._meta.get_field('text').help_text,
            'pub_date': cls.post._meta.get_field('pub_date').help_text,
        }

    def test_objects_names(self):
        group_obj = Group.objects.latest('pk')
        title = group_obj.title
        g_str = group_obj.__str__()

        for field_name, value in self.group_fields.items():
            with self.subTest(field_name=field_name):
                self.assertEqual(
                    value,
                    getattr(group_obj, field_name),
                    f'{field_name} группы неверный'
                )

        for field_name, value in self.group_verbose_fields.items():
            with self.subTest(field_name=field_name):
                self.assertEqual(
                    value,
                    group_obj._meta.get_field(field_name).verbose_name,
                    f'Verbose name {field_name} группы неверный'
                )
        for field_name, value in self.group_help_fields.items():
            with self.subTest(field_name=field_name):
                self.assertEqual(
                    value,
                    group_obj._meta.get_field(field_name).help_text,
                    f'Help text {field_name} группы неверный'
                )
        self.assertEqual(g_str, title, '__str__ группы неверный')

    def test_post_model(self):

        post_obj = Post.objects.latest('pk')
        compare_to_str = post_obj.text[:15]
        p_str = post_obj.__str__()

        for field_name, value in self.post_fields.items():
            with self.subTest(field_name=field_name):
                self.assertEqual(
                    value,
                    getattr(post_obj, field_name),
                    f'{field_name} поста неверный'
                )
        for field_name, value in self.post_verbose_fields.items():
            with self.subTest(field_name=field_name):
                self.assertEqual(
                    value,
                    post_obj._meta.get_field(field_name).verbose_name,
                    f'Verbose name {field_name} группы неверный'
                )
        for field_name, value in self.post_help_fields.items():
            with self.subTest(field_name=field_name):
                self.assertEqual(
                    value,
                    post_obj._meta.get_field(field_name).help_text,
                    f'Help text {field_name} группы неверный'
                )
        self.assertEqual(p_str, compare_to_str, '__str__ поста неверный')
