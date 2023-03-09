from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    # define setup method that will automatically run before every
    # method in the class
    def setUp(self):
        # creating a user to be referenced in all the tests
        User.objects.create_user(username='adam', password='pass')

    def test_can_list_posts(self):
        # reference user so can associate newly created post with them
        adam = User.objects.get(username='adam')
        Post.objects.create(owner=adam, title='a title')
        # you make a test network request by calling appropriate method
        # on self.client, e.g. self.client.post, self.client.put
        response = self.client.get('/posts/')
        # purposely making the test fail
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_posts(self):
        # pass in username and password from setup method
        self.client.login(username='adam', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        # count all posts and check if there's just one
        count = Post.objects.count()
        self.assertEqual(count, 1)
        # making it fail with 200_OK
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        # make it fail first
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        # creating two users and a post for each of them
        adam = User.objects.create_user(username='adam', password='pass')
        anna = User.objects.create_user(username='anna', password='pass')
        Post.objects.create(
            owner=adam, title='title 1', content='content 1'
        )
        Post.objects.create(
            owner=anna, title='title 2', content='content 2'
        )

    def test_can_retrieve_post_using_valid_id(self):
        # retrieve post with id of 1
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'title 1')
        # make it fail first
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='adam', password='pass')
        # creating a post
        response = self.client.put('/posts/1/', {'title': 'a new title'})
        # fetching the post
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/2/', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
