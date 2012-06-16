import unittest
import requests
from app.utils import Github
from mock import patch

class GitHubTestCase(unittest.TestCase):
	
	def setUp(self):
		github = Github()
		self.client_id = github.client_id
		self.secret = github.secret
		self.github = github
	
	def access_token_post(self):
		failed = 'error=bad_verification_code'
		success = 'access_token=test&token_type=bearer'
		return failed, success

	def testClientID(self):
		self.assertEquals(self.client_id, 'test_clientID')

	def testSecret(self):
		self.assertEquals(self.secret, 'test_secret')

	@patch('requests.post')
	def testAccessToken(self, MockPost):
		
		failed, success= self.access_token_post()
		failed_dict = {'error': 'bad_verification_code'}
		success_dict = {'access_token': 'test', 'token_type':'bearer'}
		
		mock = MockPost()
		mock.content = failed
		
		self.assertEquals(self.github.access_token('test'), failed_dict)
		mock.content = success
		self.assertEquals(self.github.access_token('test'), success_dict)