import requests
import json
import logging
from requests.auth import HTTPDigestAuth

logging.basicConfig(level=logging.DEBUG,format='[%(levelname)s] (%(threadName)-10s) %(message)s',)


class RestService(object):
    endpoint = ""
    username = ""
    password = ""

    """docstring for RestService"""
    def __init__(self,endpoint, username, password):
        super(RestService, self).__init__()
        self.username = username
        self.password = password
        self.endpoint = endpoint
    
    def postReadingItem(self, readingItem):
        print(readingItem.toJson())
        # response = requests.post(self.endpoint, auth = HTTPDigestAuth(self.username, self.password), verify=True, data = readingItem.toJson(), headers= {"Content-Type": "application/json"})
        response = requests.post(self.endpoint, data = readingItem.toJson(), headers= {"Content-Type": "application/json"})
        if (response.status_code == 200 or response.status_code == 201 ):
            return True
        else:
            return False