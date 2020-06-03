from django.urls import reverse
from rest_framework.test import APITestCase
from api.users.models import User
from rest_framework import status
from api.blog.models import Post, Category, Comment
from api.blog.tests.test_model_view_sets_2 import AuthenticateMixin

class MixinTest(APITestCase):
    '''
    Testing ActionPermissionMixin which consists IsAuthorPermission
    '''

    def setUp(self):
        self.credentials_test_user = {
            'username': 'testuser',
            'email': 'test@email.com',
            'password': 'testpassword'
        }
        self.credentials_author = {
            'username': 'author_test',
            'email': 'author_test@email.com',
            'password': 'author_testpassword'
        }

        self.category = Category.objects.create(name='testcategory')

        self.test_user = User.objects.create_user(**self.credentials_test_user)

        self.author = User.objects.create_user(**self.credentials_author)

        self.post = Post.objects.create(title='titletest', author=self.author, content='testcontent', category=self.category)

        self.post_list = Post.objects.all()

        self.post_1 = Post.objects.get(title='titletest')

        self.comment = Comment.objects.create(post=self.post_1, author=self.author, content='testcontent')

        self.comment_1 = Comment.objects.get(content='testcontent')

        self.comment_list = Comment.objects.all()

    def test_update_post_by_unauthorized_user(self):
        '''
        Ensure that post's updating by non-author user is forbidden
        '''
        self.client.login(username='testuser', password='testpassword')

        url = reverse('posts-detail', args=(self.post_1.pk,))

        data = {
            'title': 'title - updated',
            'content': 'content - updated',
            'category': self.category.pk
        }

        response = self.client.put(url, data=data, format='json')

        self.assertEqual(response.status_code, 403)

    def test_partial_update_post_by_unauthorized_user(self):
        '''
        Ensure that post's partial_updating by non-author user is forbidden
        '''

        self.client.login(username='testuser', password='testpassword')

        url = reverse('posts-detail', args=(self.post_1.pk,))

        data = {
            'title': 'title - updated',
        }

        response = self.client.patch(url, data=data, format='json')

        self.assertEqual(response.status_code, 403)

    def test_delete_post_by_unauthorized_user(self):
        '''
        Ensure that post's deleting by non-author user is forbidden
        '''

        self.client.login(username='testuser', password='testpassword')

        url = reverse('posts-detail', args=(self.post_1.pk,))

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 403)
        self.assertTrue(self.post_1 in self.post_list)

    def test_update_comment_by_unauthorized_user(self):
        '''
        Ensure that comment's updating by non-author user is forbidden
        '''

        self.client.login(username='testuser', password='testpassword')

        url = reverse('comments-detail', args=(self.comment_1.pk,))

        data = {
            'post': self.post_1.pk,
            'content': 'content-updated'
        }

        response = self.client.delete(url, data=data, format='json')

        self.assertEqual(response.status_code, 403)

    def test_partial_update_comment_by_unauthorized_user(self):
        '''
        Ensure that comment's partial_updating by non-author user is forbidden
        '''

        self.client.login(username='testuser', password='testpassword')

        url = reverse('comments-detail', args=(self.comment_1.pk,))

        data = {
            'content': 'content-updated'
        }

        response = self.client.delete(url, data=data, format='json')

        self.assertEqual(response.status_code, 403)

    def test_delete_comment_by_unauthorized_user(self):
        '''
        Ensure that comment's deleting by non-author user is forbidden
        '''

        self.client.login(username='testuser', password='testpassword')

        url = reverse('comments-detail', args=(self.comment_1.pk,))

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 403)
        self.assertTrue(self.comment_1 in self.comment_list)

class Test_force_authentication_mixin(AuthenticateMixin, APITestCase):

    def setUp(self):

        super().setUp()

    def test_forcing_authentication(self):

       self.assertTrue(self.test_user.is_authenticated, True)



