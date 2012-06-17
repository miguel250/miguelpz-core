import flask
import unittest
import requests
from mock import patch
from app.utils import Github
from app.core.models import Session
from app.utils import MongoSessionInterface

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