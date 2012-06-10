import os
import unittest
import tempfile
from app.api.models import User

class ViewsTestCase(unittest.TestCase):
	def setUp(self):
		User.job = 'Test Job'
		User.city = 'Test City'
		User.name = 'Test Name'
		User.github = 'Test github'
		User.twitter = 'Test twitter'
		User.linkedin = 'Test linkedin'  
		User.facebook = 'Test facebook'
		User.googleplus = 'Test googleplus'
		User.foursquare = 'Test foursquare'
		User.personal_web = 'Test personal web'
	def testMe(self):
		self.assertEquals(User.job, 'Test Job')