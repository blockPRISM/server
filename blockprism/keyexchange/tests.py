from django.test import TestCase
from django.test.client import Client


class FacebookTest(TestCase):
    def test_key_exchange(self):
        c = Client()
        response = c.post('/public_key/facebook/', {'facebook_id': 'facebook_id', 'public_key': 'public_key'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "public_key")
        response = c.get('/public_key/facebook/', {'facebook_id': 'facebook_id'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "public_key")
        response = c.post('/public_key/facebook/', {'facebook_id': 'facebook_id', 'public_key': 'public_key'})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.content, u'There is already a public key available for this facebook id.')


class GMailTest(TestCase):
    def test_key_exchange(self):
        c = Client()
        response = c.post('/public_key/gmail/', {'gmail_id': 'gmail_id', 'public_key': 'public_key'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "public_key")
        response = c.get('/public_key/gmail/', {'gmail_id': 'gmail_id'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "public_key")
        response = c.post('/public_key/gmail/', {'gmail_id': 'gmail_id', 'public_key': 'public_key'})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.content, u'There is already a public key available for this gmail email.')