from django.test import TestCase, Client

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_homepage_available(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_jupyter_notes_available(self):
        response = self.client.get('/jupyter_notes/')
        self.assertEqual(response.status_code, 200)

    def test_ppt_generator_available(self):
        response = self.client.get('/ppt_generator/')
        self.assertEqual(response.status_code, 200)