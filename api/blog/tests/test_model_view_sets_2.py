from django.urls import reverse
from rest_framework.test import APITestCase, force_authenticate
from api.users.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from api.blog.models import Post, Category, Comment

class AuthenticateMixin():
    """
    Mixin to force authentication of user for testing
    """

    def setUp(self):

        self.credentials = {
            'username': 'testuser1',
            'email': 'test1@email.com',
            'password': 'testpassword1'
        }

        self.test_user = User.objects.create_user(**self.credentials)

        self.client.force_authenticate(user=self.test_user)


class ViewSetTest(AuthenticateMixin, APITestCase):

    def setUp(self):

        super().setUp()

        self.numbers_of_post = 3


        self.category = Category.objects.create(name='testcategory')

        for post_id in range(1, self.numbers_of_post + 1):
            Post.objects.create(title=f'title{post_id}', author=self.test_user,
                                content=f'content{post_id}', category=self.category)

        self.post_1 = Post.objects.get(title='title1')
        self.post_list = Post.objects.all()

        self.comment = Comment.objects.create(post=self.post_1, author=self.test_user, content='testcontent')
        self.comment_1 = Comment.objects.get(content='testcontent')
        self.comment_list = Comment.objects.all()

    def test_post_list(self):

        url = reverse('posts-list')

        response = self.client.get(url, format='json')

        for model in self.post_list:
            self.assertIn(model.title, response.content.decode())
            self.assertIn(model.content, response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_create(self):

        url = reverse('posts-list')

        data = {
            'title': 'testtitle',
            'author': self.test_user.pk,
            'content': 'testcontent',
            'category': self.category.pk

        }

        response = self.client.post(url, data=data, follow=True)


        self.assertIn(data['title'], response.content.decode())
        self.assertIn(data['content'], response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_detail(self):


        url = reverse('posts-detail', args=(self.post_1.pk,))

        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_update(self):


        url = reverse('posts-detail', args=(self.post_1.pk,))

        data = {
            'title': 'title - updated',
            'content': 'content - updated',
            'category': self.category.pk
        }

        response = self.client.put(url, data=data, format='json', follow=True)

        self.assertIn(data['title'], response.content.decode())
        self.assertIn(data['content'], response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_partial_update(self):


        url = reverse('posts-detail', args=(self.post_1.pk,))

        data = {
            'content': 'content - updated',
        }

        response = self.client.patch(url, data=data, format='json', follow=True)

        self.assertIn(data['content'], response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_delete(self):

        url = reverse('posts-detail', args=(self.post_1.pk,))

        response = self.client.delete(url)


        self.assertFalse(self.post_1 in self.post_list)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_comment_list(self):

        url = reverse('comments-list')

        response = self.client.get(url, format='json')


        for model in self.comment_list:
            self.assertIn(model.content, response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_create(self):

        url = reverse('comments-list')

        data = {
            'post': self.post_1.pk,
            'author': self.test_user.pk,
            'content' : 'testcontent'
        }

        response = self.client.post(url, data=data, format='json')

        self.assertIn(data['content'], response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_detail(self):

        url = reverse('comments-detail', args=(self.comment.pk,))

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_update(self):

        url = reverse('comments-detail', args=(self.comment_1.pk,))

        data = {
            'post': self.post_1.pk,
            'content': 'testcontent - updated'
        }

        response = self.client.put(url, data=data, format='json', follow=True)

        self.assertIn(data['content'], response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_partial_update(self):

        url = reverse('comments-detail', args=(self.comment_1.pk,))

        data = {
            'content': 'testcontent - updated'
        }

        response = self.client.patch(url, data=data, format='json', follow=True)

        self.assertIn(data['content'], response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_delete(self):

        url = reverse('comments-detail', args=(self.comment_1.pk,))


        response = self.client.delete(url)
        self.assertFalse(self.comment_1 in self.comment_list)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


