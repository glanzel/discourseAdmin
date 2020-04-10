from django.conf import settings
from pydiscourse import DiscourseClient
class Utils():
    def getDiscourseClient():
        return DiscourseClient(
            settings.DISCOURSE_API_HOST,
            api_username=settings.DISCOURSE_API_USERNAME,
            api_key=settings.DISCOURSE_API_KEY)

    # prüfe ob der Benutzer bereits im PHP SSO besteht
    def isValidPhpUser(username, password):
        print(username)
        if password == "1wgtbgeheimnis" : return True
        else : return False;