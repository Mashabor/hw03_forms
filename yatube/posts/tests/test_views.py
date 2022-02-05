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
            text='Тестовый заголовок',
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
        first_object = response.context['page_obj'][0]
        self.assertEqual(first_object, self.post)

    def test_group_posts_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:group_posts', kwargs={'slug': self.group.slug}))
        first_object = response.context.get('group')[0]
        post_page_obj = first_object.group
        self.assertEqual(first_object, self.group)
        self.assertEqual(response.context['group'], self.post.group)


        
    