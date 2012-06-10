import os
import urls
from app.config import Settings
from app.api import views

class BaseConfig(Settings):

    def __init__(self):
        super(BaseConfig, self).__init__()

    def application(self):
        for key in urls.prints.keys():
            self.app.register_blueprint(key, url_prefix=urls.prints[key])
        return self.app
    def run(self):
        self.app.run()