import os
from flaskext.mongoengine import MongoEngine

if os.environ['ENVIRONMENT'] == 'Development':
	from development import DevelopmentConfig
	Config = DevelopmentConfig()
elif os.environ['ENVIRONMENT'] == 'Prodution':
	from prodution import ProductionConfig
	Config = ProductionConfig()
elif os.environ['ENVIRONMENT'] == 'Testing':
	from development import TestConfig
	Config = TestConfig()
	app = Config.application()
	db = MongoEngine(app)