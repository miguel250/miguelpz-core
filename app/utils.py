import requests
import json
from config import config


class Github(object):
    """Github api wrapper"""

    AUTH_ENDPOINT = 'https://github.com/login/oauth/access_token'
    HEADERS = {'content-type':'application/json'}

    def __init__(self):
        self.req = requests
        self.secret = config['GITHUB_SECRET']
        self.client_id = config['GITHUB_CLIENTID']

    def access_token(self, code):
       """Get user access token from github """

       payload = json.dumps({
        'client_id':self.client_id, 
        'client_secret':self.secret,
        'code': code,
       })

       response = requests.post(
        self.AUTH_ENDPOINT, 
        data= payload,
        headers=self.HEADERS
        )

       return dict(item.split("=") for item in  response.content.split("&"))

if __name__ == '__main__':
    print Github().access_token('b9d576e671ee73855f7f')