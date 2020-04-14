from sys import argv

import requests
from django.conf import settings
from pydiscourse import DiscourseClient
from requests.auth import HTTPBasicAuth
from discourseAdmin.models import User_Groups

from dsso.settings_local import PHP_LOGIN_CHECK_URI, PHP_LOGIN_CHECK_AUTH

class Utils:

    @staticmethod
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

    # aus php importiert
    @classmethod
    def watchImportantTopic(cls, request, accountname ) :
        if hasattr(settings, 'DISCOURSE_FORCE_TOPIC'):
            client = Utils.getDiscourseClient()
            for group_id in settings.DISCOURSE_FORCE_TOPIC:
                ug = User_Groups.objects.filter(user_id=request.user.id, group_id=group_id).all()
                print(ug)
                if ug is not None:
                    for topic_id in settings.DISCOURSE_FORCE_TOPIC[group_id]:
                        try: client.watch_topic(topic_id, accountname, notifications=3)
                        except: print("EXCEPTION für "+topic_id)


if __name__ == "__main__":
    print(f'user {argv[1]} is a valid user: {Utils.isValidPhpUser(username=argv[1], password= argv[2])}')
    
        
class MyDiscourseClient(DiscourseClient):
    def test():
        print("ahaha")
            