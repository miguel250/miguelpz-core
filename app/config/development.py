from base import BaseConfig
from flaskext.mongoengine import MongoEngine

class DevelopmentConfig(BaseConfig):
	DEBUG = True
	SECRET_KEY = '\xc8M\xcc\xc7Z\\Xe\xdb\xb1:\x8b\xfb,\xd2L*{\x81\x17$\xef\xe8\x85'
	MONGODB_DB  =  'miguelpz_dev'

	def run(self):
		self.application()
		self.app.run(host='0.0.0.0', debug=True)

app = DevelopmentConfig().application()

if __name__ == '__main__':
	DevelopmentConfig().run()