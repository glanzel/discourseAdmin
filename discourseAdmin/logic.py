from sys import argv

import requests
from django.conf import settings
from gydiscourse.pydiscourse.client import DiscourseClient
from requests.auth import HTTPBasicAuth
from discourseAdmin.models import User_Groups, Participant, User

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
            print("Try to login "+username+" by debug password")
            if password == "1wgtbgeheimnis" :
                return True
            else:
                return False

    @staticmethod
    def migrateUser(username,password):
        print("Utils.migrateUser")
        client = Utils.getDiscourseClient()
        #user = User.objects.filter(username=request.POST['username']).get()
        user,created = User.objects.get_or_create(username=username);
        user.set_password(password)
        if created :
            # TODO: gucken ob der Benutzer bereits in discourse besteht.            
            try: dUser = client.user(username)
            except: #der benutzer muss komplett erzeugt werden
                Utils.create_discourse_user(user, True)
            else: #den benutzer muss importiert werden
                Utils.import_discourse_user(dUser, user)
        return user
              

    @staticmethod
    def create_discourse_user(user, active=False): #python user sollte dann auch gerade erst erzeugt worden sein
        print("Utils.create_discourse_user")
        client = Utils.getDiscourseClient()
        if active != True : user.is_active = False
        #email für python nutzer anlegen
        if hasattr(settings, 'DISCOURSE_INTERN_SSO_EMAIL') :
            user.email = '%s%s@%s' % ("da", user.id, settings.DISCOURSE_INTERN_SSO_EMAIL)
        user.save()
              
        #der benutzer wird in discourse erzeugt. 
        dUser = client.create_user(user.username, user.username, user.email, user.password)
        if active : client.activate(dUser['user_id'])
          
        #die verbindung zu discourse wird angelegt                    
        p = Participant(user = user, discourse_user=dUser['user_id'])
        p.save();

    @staticmethod
    def import_discourse_user(dUser, user) :
        print("Utils.import_discourse_user")
        client = Utils.getDiscourseClient()
        userDetails = client.user_all(user_id=dUser['id'])
        ssoDetails = userDetails['single_sign_on_record']         
        if ssoDetails != None :
            print(ssoDetails['external_email'])
            user.email = ssoDetails['external_email']

        for key in dUser:
            if key != "id":
                try: setattr(user, key, dUser[key])
                except: print(getattr(user,key))

        if 'suspended_at' in userDetails : 
            user.is_active = False;

        user.save();
        try:
            p = user.participant
        except:
            p = Participant(user = user)
        p.discourse_user=dUser['id']
        p.save();
        return user;

    @staticmethod
    def import_dgroup_members(groupname, da_group_id, limit=1000, offset=0):
        print("member auslesen");
        client = Utils.getDiscourseClient()
        members = client.group_members(groupname, limit=limit, offset=offset)

        for member in members:
            print(member['username'])

            # nutzer in da erstellen falls noch nicht vorhanden
            user, u_created = User.objects.get_or_create(username=member['username'])
            #if u_created :
            user = Utils.import_discourse_user(member,user)

            #print(user.__dict__)

            # nutzer in da zu gruppe hinzufügen
            try: p = user.participant
            except: p = Participant(user = user)
            p.discourse_user=member['id']
            p.save();

            try: ug, ug_created = User_Groups.objects.get_or_create(user_id=p.user_id, group_id = da_group_id)
            except : 
                print( f'Benutzer {p.user_id} scheint doppelt in Gruppe {da_group_id} vorzukommen versuche zu reparieren')
                Utils.delete_double_ug(user_id=p.user_id, group_id = da_group_id)
            else:    
                if ug_created:
                    print(f'Fuege Benutzer {p.user_id} zur Gruppe hinzu')
                    ug.save()    

    @staticmethod
    def delete_double_ug(user_id, group_id):
        ugs = User_Groups.objects.filter(user_id=user_id, group_id = group_id)
        print(ugs)
        no = 0
        for ug in ugs :
            if no == 0 : print("keep first occurance")
            else : 
                print("delete other occurance")
                ug.delete()
            no = no+1
            
    
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
            