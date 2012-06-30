import unittest
import requests
from mock import patch
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
            personal_web =  'Test personal web',
            )
        user = user.save()
        self.user = user
        self.id = user.id

    def testUserSettingsLoading(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.id
            rv = c.get('/user/settings')

            self.assertEquals(rv.status_code, 200)
            self.assertTrue('Test username' in rv.data)
            self.assertTrue('Test email' in rv.data)
            self.assertTrue('Test Job' in rv.data)
            self.assertTrue('Test City' in rv.data)
            self.assertTrue('Test Name'  in rv.data)
            self.assertTrue('Test github' in rv.data)
            self.assertTrue('Test twitter'  in rv.data)
            self.assertTrue('Test linkedin' in rv.data)
            self.assertTrue('Test facebook' in rv.data)
            self.assertTrue('Test googleplus' in rv.data)
            self.assertTrue('Test foursquare' in rv.data)
            self.assertTrue('Test personal web' in rv.data)

    def testUserSettingSave(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.id

            post = dict(
                    username = 'Test username 2',
                    email = 'Test@test.com',
                    job = 'Test Job 2',
                    city = 'Test City 2',
                    name = 'Test Name 2',
                    github = 'Test github 2',
                    twitter = 'Test twitter 2',
                    linkedin = 'Test linkedin 2',
                    facebook   = 'Test facebook 2',
                    googleplus = 'Test googleplus 2',
                    foursquare = 'Test foursquare 2',
                    personal_web = 'Test personal web 2',
                )
            rv = c.post('/user/settings', data=post)

            self.assertEquals(rv.status_code, 200)
            self.assertTrue('Test username 2' in rv.data)
            self.assertTrue('Test@test.com' in rv.data)
            self.assertTrue('Test Job 2' in rv.data)
            self.assertTrue('Test City 2' in rv.data)
            self.assertTrue('Test Name 2'  in rv.data)
            self.assertTrue('Test github 2' in rv.data)
            self.assertTrue('Test twitter 2'  in rv.data)
            self.assertTrue('Test linkedin 2' in rv.data)
            self.assertTrue('Test facebook 2' in rv.data)
            self.assertTrue('Test googleplus 2' in rv.data)
            self.assertTrue('Test foursquare 2' in rv.data)
            self.assertTrue('Test personal web 2' in rv.data)

            user = User.objects(id=self.id).first()

            self.assertEquals(post['username'], user.username)
            self.assertEquals(post['email'], user.email )
            self.assertEquals(post['job'], user.job)
            self.assertEquals(post['city'], user.city)
            self.assertEquals(post['name'], user.name)
            self.assertEquals(post['github'], user.github)
            self.assertEquals(post['twitter'], user.twitter)
            self.assertEquals(post['linkedin'], user.linkedin)
            self.assertEquals(post['facebook'], user.facebook)
            self.assertEquals(post['googleplus'], user.googleplus)
            self.assertEquals(post['foursquare'], user.foursquare)
            self.assertEquals(post['personal_web'], user.personal_web)


    def testLogin(self):
        rv = self.app.get('/login/')
        self.assertEquals(rv.status_code, 200)
        
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