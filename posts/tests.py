from django.test import TestCase, Client
from users.forms import User
from posts.models import Post

#class TestStringMethods(TestCase):
#        def test_length(self):
#                self.assertEqual(len("yatube"), 6)

#        def test_show_msg(self):
#                # действительно ли первый аргумент — True?
#                self.assertTrue(False, msg="Важная проверка на истинность")

class TestYatube(TestCase):
        def setUp(self):
                self.client = Client()
                self.user = User.objects.create_user(
                        username = 'test', email = 'test@test.ru', password = 'test123456'
                )
                self.post = Post.objects.create(text="Этот пост создан для теста", author=self.user)
        def test_profile(self):
                response = self.client.get('/test/')  
                self.assertEqual(response.status_code, 200)

        def test_post(self):
                self.client.post('/auth/login/', {'username': 'test', 'password': 'test123456'}) 
                self.post = Post.objects.create(text="Этот пост создан для теста", author=self.user)
                response_new = self.client.get('/test/')
                self.assertIn("page", response_new.context)
        def test_post_no_auth(self):
                self.client.logout()
                self.post = Post.objects.create(text="Этот пост создан для теста", author=self.user)
                response_new = self.client.get('/test/')
                self.assertIn("page", response_new.context)
        

                