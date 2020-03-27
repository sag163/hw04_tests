from django.test import TestCase, Client
from users.forms import User
from posts.models import Post



class TestYatube(TestCase):
        def setUp(self):
                self.client = Client()
                self.user = User.objects.create_user(
                        username = 'test', email = 'test@test.ru', password = 'test123456'
                )
                self.client.post('/auth/login/', {'username': 'test', 'password': 'test123456'}) 
        
        
        def test_profile(self):
                response = self.client.get('/test/')  
                self.assertEqual(response.status_code, 200)

        def test_post(self):
                self.post = Post.objects.create(text="test_text", author=self.user)
                response = self.client.get('/test/')
                self.assertContains(response, "test_text")


        def test_post_no_auth(self):
               self.client.logout()
               response = self.client.get('/new/')  
               self.assertRedirects(response, '/auth/login/?next=/new/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        def test_public_post(self):
                post = Post.objects.create(text="Тестовый пост!", author=self.user)
                response = self.client.get('/')
                self.assertContains(response, "Тестовый пост!")
                response = self.client.get('/test/')
                self.assertContains(response, "Тестовый пост!")
                response = self.client.get(f'/test/{post.id}/')
                self.assertContains(response, "Тестовый пост!")

        def test_edit_post(self):
                self.client.post('/new/', {'text':"Тестовый пост!"}, follow=True)
                post = Post.objects.get(author=self.user)
                self.client.post(f'/test/{post.id}/edit', {'text':"Тестовый пост (Редакция №1)!"}, follow=True)
                response = self.client.get('/')
                self.assertContains(response, "Тестовый пост (Редакция №1)!")
                response = self.client.get('/test/')
                self.assertContains(response, "Тестовый пост (Редакция №1)!")
                response = self.client.get(f'/test/{post.id}/')
                self.assertContains(response, "Тестовый пост (Редакция №1)!")
        


                