import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, override_settings
from django.urls import reverse

from ..models import Comment, Post, Group

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

user = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestF(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = user.objects.create_user(username='FUser')
        cls.user2 = user.objects.create_user(username='AnotherFUser')
        cls.group = Group.objects.create(
            title='FTestGroup',
            slug='FTG',
            description='FDESC'
        )
        cls.test_post = Post.objects.create(
            text='TEST EDIT TEXT',
            group=cls.group,
            author=cls.user,
        )
        cls.cl = Client()
        cls.cl.force_login(cls.user)
        cls.cl2 = Client()
        cls.cl2.force_login(cls.user2)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_post_create(self):

        local_username = self.user.username
        local_group = self.group
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=b'\x47\x49\x46\x38\x39\x61\x02\x00'
                    b'\x01\x00\x80\x00\x00\x00\x00\x00'
                    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
                    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
                    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
                    b'\x0A\x00\x3B',
            content_type='image/gif'
        )
        post_form = {
            'text': 'TEST ENTRY',
            'group': local_group.pk,
            'image': uploaded,
        }

        response = self.cl.post(
            reverse('posts:post_create'),
            data=post_form,
            follow=True
        )
        post_entry = Post.objects.latest('pk')
        self.assertEqual(post_form['text'], post_entry.text)
        self.assertEqual(local_group, post_entry.group)
        self.assertTrue(post_entry.image)
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': f'{local_username}'})
        )

        post_on_profile_page = response.context.get('page_obj')[0]
        self.assertEqual(
            post_entry.pk,
            post_on_profile_page.pk
        )

        response = self.client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': f'{local_group.slug}'}
            )
        )

        post_on_group_page = response.context.get('page_obj')[0]
        self.assertEqual(
            post_entry.pk,
            post_on_group_page.pk
        )

        response = self.client.get(reverse('posts:index'))

        post_on_index_page = response.context.get('page_obj')[0]
        self.assertEqual(
            post_entry.pk,
            post_on_index_page.pk
        )

        count_before_add_anon = Post.objects.count()
        response = self.client.post(
            reverse('posts:post_create'),
            data=post_form,
            follow=True
        )
        count_after_add_anon = Post.objects.count()
        self.assertEqual(
            count_before_add_anon,
            count_after_add_anon,
            'Post added with anon user!'
        )
        self.assertRedirects(
            response,
            reverse('users:login') + '?next=' + reverse('posts:post_create')
        )

    def test_post_edit(self):
        new_text = 'CHANGED!'
        response = self.cl.post(
            reverse(
                'posts:post_edition',
                kwargs={'post_id': f'{self.test_post.pk}'}
            ),
            data={'text': new_text}, follow=True
        )

        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': f'{self.test_post.pk}'}
            )
        )
        changed_post = Post.objects.get(pk=self.test_post.pk)
        self.assertEqual(new_text, changed_post.text)

    def test_post_edit_diff_user(self):

        local_group = self.group
        check_text = 'Some new text'
        response = self.cl2.post(
            reverse(
                'posts:post_edition',
                kwargs={'post_id': f'{self.test_post.pk}'}
            ),
            data={'text': check_text, 'group': local_group.pk},
            follow=True
        )
        check_post = Post.objects.latest('pk')
        self.assertEqual(check_post.text, self.test_post.text)
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': f'{self.test_post.pk}'}
            )
        )

        response = self.client.post(
            reverse(
                'posts:post_edition',
                kwargs={'post_id': f'{self.test_post.pk}'}
            ),
            data={'text': check_text, 'group': local_group.pk},
            follow=True
        )
        self.assertEqual(check_post.text, self.test_post.text)

    def test_comment_add(self):
        local_post = self.test_post

        comment_form = {
            'text': 'TEST COMMENT',
            'post': local_post,
        }

        response = self.cl.post(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': f'{local_post.pk}'}
            ),
            data=comment_form,
            follow=True
        )
        comm_entry = Comment.objects.latest('pk')
        self.assertEqual(comment_form['text'], comm_entry.text)
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': f'{local_post.pk}'}
            )
        )

        comm_on_post_page = response.context.get('comments').all()[0]
        self.assertEqual(
            comm_entry.pk,
            comm_on_post_page.pk
        )

    def test_comment_add_anon(self):
        local_post = self.test_post

        comment_form = {
            'text': 'TEST COMMENT',
            'post': local_post,
        }

        response = self.client.post(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': f'{local_post.pk}'}
            ),
            data=comment_form,
            follow=True
        )
        comm_count = Comment.objects.count()
        self.assertRedirects(
            response,
            reverse('users:login') + '?next=' + reverse(
                'posts:add_comment',
                kwargs={'post_id': f'{local_post.pk}'}
            )
        )
        self.assertEqual(comm_count, 0, 'Комментарий добавлен')
