import flask
import unittest
import requests
from mock import patch
from app.core.models import Session
from app.utils import Github, MongoSessionInterface, UserAuth

class UserAuthTestCase(unittest.TestCase):
	
	def setUp(self):
		self.user_auth = UserAuth()

	def tearDown(self):
		Session.drop_collection()

	def testIsAuthenticated(self):
		app = flask.Flask(__name__)
		app.session_interface = MongoSessionInterface()
		with app.test_request_context():
			flask.session['user_id'] = 'test_id'
			self.assertTrue(self.user_auth.is_authenticated())
			flask.session.pop('user_id', None)
			self.assertFalse(self.user_auth.is_authenticated())
	def testIsAnonymous(self):
		app = flask.Flask(__name__)
		app.session_interface = MongoSessionInterface()
		with app.test_request_context():
			flask.session['user_id'] = 'test_id'
			self.assertFalse(self.user_auth.is_anonymous())
			flask.session.pop('user_id', None)
			self.assertTrue(self.user_auth.is_anonymous())

	def testLoginRequiredURL(self):
		app = flask.Flask(__name__)
		app.debug = True
		app.session_interface = MongoSessionInterface()

		user_auth_1 = UserAuth('.login')
		@app.route('/login/')
		def login():
			messages = flask.get_flashed_messages()
			return messages[0]
		c = app.test_client()

		@app.route('/admin/')
		@user_auth_1.login_required
		def get():
			return 'secret'
		assert 'secret' not in c.get('/admin/').data
		self.assertEquals(c.get('/admin/',  follow_redirects=True).data, 'You most login to see this page')

	def testLoginRequireNone(self):
		app = flask.Flask(__name__)
		app.debug = True
		app.session_interface = MongoSessionInterface()

		user_auth = self.user_auth

		@app.route('/admin/')
		@user_auth.login_required
		def get():
			return 'secret'
		c = app.test_client()
		assert 'secret' not in c.get('/admin/').data

class MongoSessionTestCase(unittest.TestCase):

	def tearDown(self):
		Session.drop_collection()

	def testMongoDataCreate(self):
		app = flask.Flask(__name__)
		app.session_interface = MongoSessionInterface()
		with app.test_request_context():
			id = flask.session.sid
			flask.session['test_data'] = 'test'
			session = Session.objects(session_id=id).first()
			self.assertEquals(flask.session['test_data'], session.data['test_data'])
	
	def testMongoDataDelete(self):
		app = flask.Flask(__name__)
		app.session_interface = MongoSessionInterface()
		with app.test_request_context():
			id = flask.session.sid
			flask.session['test_data'] = 'test'
			flask.session.pop('test_data', None)
			session = Session.objects(session_id=id).first()
			self.assertEquals(flask.session.get('test_data'), session.data.get('test_data'))

	def testCreateSession(self):
		app = flask.Flask(__name__)
		app.session_interface = MongoSessionInterface()

		@app.route('/create/session')
		def get():
			flask.session['value'] = 'test_session'
			return flask.session['value']
		c = app.test_client()
		self.assertEquals(c.get('/create/session').data, 'test_session')

	def testDeleteSession(self):
		app = flask.Flask(__name__)
		app.session_interface = MongoSessionInterface()

		def expect_exception(f, *args, **kwargs):
			try:
				f(*args, **kwargs)
			except KeyError, e:
				self.assert_(e.args and 'Key not in this session' in e.args[0])
			else:
				self.assert_(False, 'expected exception')

		with app.test_request_context():
			self.assertEquals(flask.session.get('missing_key'), None)
			expect_exception(flask.session.pop, 'foo')

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