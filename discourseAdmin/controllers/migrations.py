import pdb, json, sys
import logging
import datetime

from django.core import serializers #benutzen wir das ?
from django.core.exceptions import ValidationError
from django.conf import settings

#from django.contrib import auth
#from django.contrib.auth import password_validation
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
#from django.urls import reverse
from django.middleware.csrf import get_token

from discourseAdmin.models import Participant, User, dGroup
from discourseAdmin.forms import UserForm, LoginForm, ChangePasswordForm, GroupForm
from discourseAdmin.logic import Utils

from django3scaffold.http import JsonResponse # TODO: wieder ausbauen zugunsten der std JsonResponse ?
from datetime import date

logger = logging.getLogger(__name__)


# migration only - später verschieben oder löschen
@staff_member_required
def fix_users_email(request):

    users = User.objects.all().filter(email="")
    for user in users:
        print(user.username)
        client = Utils.getDiscourseClient()
        try:
            dUser = client.user(username=user.username)
        except: print ("Der Benutzer "+user.username+" scheint nicht sinvoll mit discourse verknüpft zu sein")
        else :
            emails = client.user_emails(user.username)
            user.email = emails['email']
            print(emails['email'])
            user.save()

    return JsonResponse()

# migration only später verschieben oder löschen
@staff_member_required
def init_set_departments(request):

    users = User.objects.all()
    for user in users:
        try: 
            if user.participant.department is None:
                groups = user.dgroup_set.all()
                for group in groups:
                    if group.is_department:
                         user.participant.department = group;
                         print(user)
                         print(user.participant.department)
                         user.participant.save()
            else:
                None 
        except: None
        
        #dgroup = dGroup.objects.get(id=group_id) 
        #otheruser = User.objects.get(id=user_id)
        #otheruser.participant.department = dgroup

    return JsonResponse()


from django.core.serializers.json import DjangoJSONEncoder
@staff_member_required
#import_dgroups aktualisiert von discourse -> discourseAdmin (bitte vorsichtig verwenden)    
def import_dgroups(request):
    client = Utils.getDiscourseClient()
    groupsDict = client.groups()
    for groupDict in groupsDict:
        # gruppe in da erzeugen falls noch nicht vorhanden
        groupObj, created = dGroup.objects.get_or_create(discourse_group_id=groupDict['id'])
        if groupDict['automatic'] & (groupDict['name'] != "vertrauensstufe_0") :
            groupObj.delete();
        else:    
            print("import: "+str(groupDict['id'])+" : "+groupDict['name'])
            if created: 
                print("created")
                for key in groupDict:
                    if key != "id":
                        setattr(groupObj, key, groupDict[key])
                groupObj.create_date = datetime.datetime.now()
            else: 
                print("already exists") #TODO: Discourse group aktualisieren ?      
                #groupObj.update_date = datetime.datetime.now()
            groupObj.discourse_group_id = groupDict['id']         
            groupObj.save();
            Utils.import_dgroup_members(groupDict['name'], groupObj.id)

    return JsonResponse()

@staff_member_required    
def import_dgroup(request, groupname, da_group_id):
    limit = request.GET.get("limit") if request.GET.get("limit") else 1000
    offset = request.GET.get("offset") if request.GET.get("offset") else 0
    client = Utils.getDiscourseClient()
    Utils.import_dgroup_members(groupname, da_group_id, limit, offset)
    return JsonResponse()

@staff_member_required    
def import_users(request):
    client = Utils.getDiscourseClient()
    usersDict = client.users()
    for userDict in usersDict:
        userObj, created = User.objects.get_or_create(username=userDict['username'])

        print(userDict)
        #print(created)
        
        if 'suspended_at' in userDict : 
            userObj.is_active = False;
            userObj.save();
            

        
        if created: 
        # wenn der benutzer per login erzeugt wurde muss er hier aktualisiert werden
            userDetails = client.user_all(user_id=userDict['id'])
            ssoDetails = userDetails['single_sign_on_record']         
            if ssoDetails != None :
                print(ssoDetails['external_email'])
                userObj.email = ssoDetails['external_email']
    
            for key in userDict:
                if key != "id":
                    setattr(userObj, key, userDict[key])

            if not userDetails['active'] : 
                userObj.is_active = False;
    
            userObj.save();

        else : None
            #TODO overwrite Userdata in Discourse
            #print("TODO")
        
        try:
            p = userObj.participant
        except:
            p = Participant(user = userObj)
        p.discourse_user=discourse_user=userDict['id']
        p.save();
             
        print(userDict)
        print("-");
        print(userObj.__dict__)
        print("-");
    return JsonResponse()
    #return JsonResponse(usersDict, DjangoJSONEncoder,False) #warum geht das nicht es sollte korrekt sein
