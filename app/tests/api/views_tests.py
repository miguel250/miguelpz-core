import os
import unittest
import tempfile
import json
from app.config.run import app
from app.core.models import User

class ViewsTestCase(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
		user = User(
			username = 'Test username',
			email = 'Test email',
			job = 'Test Job',
			city = 'Test City',
			name = 'Test Name',
			github = 'Test github',
			twitter = 'Test twitter',
			linkedin = 'Test linkedin',
			facebook = 'Test facebook',
			googleplus = 'Test googleplus',
			foursquare = 'Test foursquare',
			personal_web =  'Test personal web'
			)
		user = user.save()
		self.id = user.id

	def testMe(self):
		user ={
			'status': 200,
        	'info': {
            	'job': 'Test Job',
            	'name': 'Test Name',
            	'city': 'Test City',
            	'pesonal_website': 'Test personal web'
        	},
        	'social' : {
            	'github': 'Test github',
            	'twitter': 'Test twitter',
            	'linkedin': 'Test linkedin',
            	'facebook': 'Test facebook',
            	'googleplus': 'Test googleplus',
            	'foursquare': 'Test foursquare',
            	'personal_web': 'Test personal web'
        	},
    	}
		rv = self.app.get('/api/me/%s'%self.id)
		data = json.loads(rv.data)
		self.assertEquals(data, user)

	def testError(self):
		rv = self.app.get('/api/m')
		self.assertEquals(rv.status_code, 404)