from django.contrib.contenttypes.models import ContentType
from mixer.backend.django import mixer

from rest_framework.reverse import reverse

from social_media.tests import BaseAPITest
from posts.models import Post, Like


class TestPostViewSet(BaseAPITest):

    def setUp(self):
        self.user = self.create_and_login()
        self.user1 = self.create(email='hello@example.com')

        self.post = mixer.blend(Post, user=self.user)
        self.post1 = mixer.blend(Post, user=self.user1)

        self.data = {
            "title": "title123",
            "body": "body",
        }

    def test_list_posts(self):
        resp = self.client.get(reverse('v1:posts:posts-list'))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data['results']), 2)
        self.assertEqual(resp.data['results'][0]['id'], self.post1.id)
        self.assertEqual(resp.data['results'][1]['id'], self.post.id)

    def test_list_posts_unauthorized(self):
        self.logout()
        resp = self.client.get(reverse('v1:posts:posts-list'))
        self.assertEqual(resp.status_code, 401)

    def test_retrieve_post(self):
        resp = self.client.get(reverse('v1:posts:posts-detail', args=(self.post.id,)))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['id'], self.post.id)
        self.assertEqual(resp.data['title'], self.post.title)

    def test_retrieve_post_unauthorized(self):
        self.logout()
        resp = self.client.get(reverse('v1:posts:posts-detail', args=(self.post.id,)))
        self.assertEqual(resp.status_code, 401)

    def test_retrieve_post_of_other_user(self):
        resp = self.client.get(reverse('v1:posts:posts-detail', args=(self.post1.id,)))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['id'], self.post1.id)
        self.assertEqual(resp.data['body'], self.post1.body)

    def test_create_post(self):
        resp = self.client.post(reverse('v1:posts:posts-list'), data=self.data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['title'], self.data['title'])
        self.assertEqual(resp.data['body'], self.data['body'])

        post = Post.objects.get(title=self.data['title'], user=self.user)
        self.assertEqual(post.body, self.data['body'])

    def test_create_post_unauthorized(self):
        self.logout()
        resp = self.client.post(reverse('v1:posts:posts-list'), data=self.data)
        self.assertEqual(resp.status_code, 401)

    def test_update_post(self):
        self.data = {
            "body": "new_body",
            "title": "new_title",
        }
        resp = self.client.put(reverse('v1:posts:posts-detail', args=(self.post.id,)),
                               data=self.data)
        self.assertEqual(resp.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(resp.data['body'], self.data['body'])
        self.assertEqual(resp.data['title'], self.data['title'])

        self.assertEqual(self.post.title, self.data['title'])
        self.assertEqual(self.post.body, self.data['body'])

    def test_destroy_post(self):
        resp = self.client.delete(reverse('v1:posts:posts-detail', args=(self.post.id,)))
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_like_post_exist(self):
        obj_type = ContentType.objects.get_for_model(Post)
        Like.objects.create(content_type=obj_type, object_id=self.post.id, user=self.user)
        resp = self.client.post(reverse('v1:posts:posts-like', args=(self.post.id,)))
        self.assertEqual(resp.status_code, 204)
