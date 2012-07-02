import os
import unittest
import json
from app.config.run import app
from app.config import mail
from app.core.models import User

class ViewsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        user = User(
            username = 'Test username',
            email = 'test@test.com',
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
        self.username = user.username
    
    def tearDown(self):
        User.drop_collection()
    
    def testContactError(self):
        post = {
           'email': '',
           'name': '',
           'subject':  '',
           'body': ''
        }

        rv = self.app.post('/api/me/contact/%s'%self.username,  data=json.dumps(post))
        data = json.loads(rv.data)

        self.assertEquals(data['status'], 422)
        self.assertTrue(data['email']['error'])
        self.assertTrue(data['name']['error'])
        self.assertTrue(data['subject']['error'])
        self.assertTrue(data['body']['error'])

    def testContactSuccess(self):
        post = {
           'email': 'test@test.com',
           'name': 'test_name',
           'subject':  'test_name',
           'body': 'test_body'
        }

        with mail.record_messages() as outbox:
            rv = self.app.post('/api/me/contact/%s'%self.username,  data=json.dumps(post))
            data = json.loads(rv.data)

            self.assertEquals(data['status'], 200)
            self.assertTrue(post['name'] in rv.data)
            self.assertEquals(outbox[0].subject, post['subject'])
            self.assertEquals(outbox[0].recipients, [post['email']])
            self.assertEquals(outbox[0].body, post['body'])
        
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
        rv = self.app.get('/api/me/%s'%self.username)
        data = json.loads(rv.data)
        self.assertEquals(data, user)

    def testError(self):
        rv = self.app.get('/api/m')
        self.assertEquals(rv.status_code, 404)