from django.urls import reverse
from rest_framework.test import APITestCase
from api.users.models import User
from rest_framework import status
from api.blog.models import Post, Category, Comment
from api.blog.tests.test_model_view_sets_2 import AuthenticateMixin

class FiltersTestCase(AuthenticateMixin, APITestCase):

    def setUp(self):

        super().setUp()

        self.numbers_of_post = 10

        self.category = Category.objects.create(name='testcategory')

        for post_id in range(1, self.numbers_of_post + 1):
            Post.objects.create(title=f'title{post_id}', author=self.test_user,
                                content=f'content{post_id}', category=self.category)

        self.post_5 = Post.objects.get(title='title5')
        self.post_exact_date_posted = self.post_5.date_posted


    def test_post_list_filter_by_title(self):

        url = f"{reverse('posts-list')}?title=title2"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


    def test_post_list_filter_by_date_posted_iexact(self):

        date = self.post_exact_date_posted

        url = f"{reverse('posts-list')}?date_posted_iexact=date"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_post_list_filter_by_date_posted_lte(self):

        date = self.post_exact_date_posted

        url = f"{reverse('posts-list')}?date_posted_lte=date"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_post_list_filter_by_date_posted_gte(self):

        date = self.post_exact_date_posted

        url = f"{reverse('posts-list')}?date_posted_gte=date"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)