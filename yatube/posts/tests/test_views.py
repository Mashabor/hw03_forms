from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from ..models import Post, Group

User = get_user_model()

class PostViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TrueName')
        cls.group = Group.objects.create(
            title='test-title',
            description='test-description',
            slug='test-slug'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='test-text',
            pub_date='04.02.2022'
        )

        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse('posts:group_posts', kwargs={'slug': 'test-slug'}),
            'posts/profile.html': reverse('posts:profile', kwargs={'username': 'TrueName'}),
            'posts/post_detail.html': reverse('posts:post_detail', kwargs={'post_id': '1'}),
            'posts/post_create.html': reverse('posts:post_create'),
            'posts/post_create.html': reverse('posts:post_edit', kwargs={'post_id': '1'}),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

        
    def test_index_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(
            response.context['page_obj'][0], self.post
        )

    def test_group_posts_page_show_correct_context(self):
        response = self.authorized_client.get(reverse(
            'posts:group_posts', kwargs={'slug': 'test-slug'}
        ))
        self.assertEqual(
            response.context['page_obj']
            [0].author.username,
            'TrueName'
        )
        self.assertEqual(
            response.context['page_obj']
            [0].text,
            'test-text'
        )
        self.assertEqual(
            response.context['page_obj']
            [0].group.title,
            'test-title'
        )
        self.assertEqual(response.context['group'], self.group)

    def test_profile_page_show_correct_context(self):
        response = self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': 'TrueName'}
        ))
        self.assertEqual(
            response.context['page_obj']
            [0].author.username,
            'TrueName'
        )
        self.assertEqual(
            response.context['page_obj']
            [0].text,
            'test-text'
        )
        self.assertEqual(
            response.context['page_obj']
            [0].group.title,
            'test-title'
        )
        self.assertEqual(response.context['author'], self.user)

    def test_post_detail_page_show_correct_context(self):
        response = self.authorized_client.get(reverse(
            'posts:post_detail', kwargs={'post_id': '1'}
        ))
        self.assertEqual(response.context['post'], self.post)

    def test_post_create_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField
        }        
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_show_correct_context(self):
        response = self.authorized_client.get(reverse(
            'posts:post_edit', kwargs={'post_id': '1'}
        ))
        form_fields = {
            'text': forms.fields.CharField
        }        
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)