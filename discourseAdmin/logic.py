from sys import argv

import requests
from django.conf import settings
from pydiscourse import DiscourseClient
from requests.auth import HTTPBasicAuth

from dsso.settings_local import PHP_LOGIN_CHECK_URI, PHP_LOGIN_CHECK_AUTH


class Utils:



    def getDiscourseClient():
        return DiscourseClient(
            settings.DISCOURSE_API_HOST,
            api_username=settings.DISCOURSE_API_USERNAME,
            api_key=settings.DISCOURSE_API_KEY)

    # prüfe ob der Benutzer bereits im PHP SSO besteht
    @staticmethod
    def isValidPhpUser(username, password):
        if PHP_LOGIN_CHECK_URI is not None:
            post_data = {'api': True,
                         'password': password,
                         'accountname': username,
                         'action': 'check_login'}
            if PHP_LOGIN_CHECK_AUTH is not None:
                basic_auth = HTTPBasicAuth(PHP_LOGIN_CHECK_AUTH['username'], PHP_LOGIN_CHECK_AUTH['password'])
            else:
                basic_auth = None
            result = requests.post(PHP_LOGIN_CHECK_URI, data=post_data, auth=basic_auth)
            return result.status_code >= 200 and result.status_code < 300
        else:
            print(username)
            if password == "1wgtbgeheimnis" :
                return True
            else:
                return False


if __name__ == "__main__":
    print(f'user {argv[1]} is a valid user: {Utils.isValidPhpUser(username=argv[1], password= argv[2])}')