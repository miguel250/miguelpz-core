import urls
from app.config import Settings

class Run(Settings):
    
    def __init__(self):
        super(Run, self).__init__()
    
    def application(self):
        self.environment()
        for key in urls.prints.keys():
            self.app.register_blueprint(key, url_prefix=urls.prints[key])
        return self.app
    
    def run(self):
        self.application()
        self.app.run(host='0.0.0.0', debug=True)

run = Run()
app = run.application()