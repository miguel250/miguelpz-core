import unittest
import requests
from mock import patch
from app.config.run import app


class ViewsTestCase(unittest.TestCase):

	def setUp(self):
		self.app = app.test_client()

	@patch('requests.post')
	def testCallback_error(self, mockPost):
		mock = mockPost()
		mock.content = 'error=bad_verification_code'
		rv = self.app.get('/callback?type=github&code=error',  follow_redirects=True)
		assert 'An error has occurred:' in rv.data

	def testCallbackCode(self):
		rv = self.app.get('/callback?type=github',  follow_redirects=True)
		assert 'Invalid verification code' in rv.data

	def testCallbackUnknown(self):
		rv = self.app.get('/callback?type=unknown',  follow_redirects=True)
		assert 'Unknown authentication type'in rv.data

	def testNoAthentication(self):
		rv = self.app.get('/callback',  follow_redirects=True)
		assert 'Authentication type missing'in rv.data