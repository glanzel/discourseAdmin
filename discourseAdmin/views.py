import pdb, json, sys
import logging #benutzen wir das ?
import datetime
#from django.forms.models import model_to_dict
from django.core import serializers #benutzen wir das ?
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.middleware.csrf import get_token
from django3scaffold.http import JsonResponse # TODO: wieder ausbauen zugunsten der std JsonResponse ?
from discourseAdmin.models import Participant, User
from discourseAdmin.forms import UserForm, LoginForm, ChangePasswordForm
from discourseAdmin.logic import Utils
from doctest import DebugRunner #wird das benutzt ?
from django.conf import settings
from django.contrib import messages
from pip._vendor.colorama.ansi import Fore # was macht das ?
from gydiscourse.pydiscourse.client import DiscourseClient
from gydiscourse.pydiscourse.exceptions import DiscourseClientError

#from lib2to3.pgen2.tokenize import group # wo kommt das her ?
#from __builtin__ import True # und was soll das  ?

sso_links = {'anmeldung':'Login', 'create_user':'Registrieren', 'change_password':'Passwort ändern', 'user-list':'Login:Adminbereich'}

@login_required
def user_list(request, template='user/list.html'):
    d = {}

    d['user_list'] = User.objects.all().order_by('-date_joined', '-last_login')
    if request.method == 'GET':
        filters = {}
        for key in request.GET:
            if request.GET[key] == 'True': filters[key] = True
            if request.GET[key] == 'False': filters[key] = False
        d['user_list'] = d['user_list'].filter(**filters)
    return render(request, template, d)

from discourseAdmin.forms import UserForm
@login_required
def user_edit(request, id, template='user/edit.html'):
    #TODO: wieder einbauen ?
    return JsonResponse()
    d = {}
    item = get_object_or_404(User, pk=id)
    print(serializers.serialize('json', [ item, ]))
    #pdb.set_trace()
    d['form'] = UserForm(instance=item)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            return JsonResponse(data={'form': UserForm(instance=item).as_p(), 'token': get_token(request)})
        else:
            d['form'] = form
            return JsonResponse(data={'form': d['form'].as_p(), 'token': get_token(request)}, success=False)
    d['user'] = User.objects.get(pk=id)
    return render(request, template, d)

from discourseAdmin.forms import HasDiscoGroups
@login_required
def user_details(request, id, template='user/details.html'):
    d = {}
    item = get_object_or_404(User, pk=id)
    d['user_groups'] = item.dgroup_set.all()
 
    d['admin_groups'] = dGroup.objects.all().filter(user_groups__rights=1, user_groups__user_id=request.user.id).exclude(id__in=d['user_groups'])
    d['form'] = HasDiscoGroups()
  
    
    if request.method == 'POST':
        print(request.POST)
        form = HasDiscoGroups(request.POST, instance=item)
        print(serializers.serialize('json', [ item, ]))
        if form.is_valid():
            print(form.cleaned_data)
            item = form.save()
            #form.save_m2m()
            return JsonResponse(data={'form': UserForm(instance=item).as_p(), 'token': get_token(request)})
        else:
            d['form'] = form
            return JsonResponse(data={'form': d['form'].as_p(), 'token': get_token(request)}, success=False)
    d['user'] = User.objects.get(pk=id)
    return render(request, template, d)

@login_required
def user_delete(request, id):
    #TODO: wieder einbauen ?
    return JsonResponse()
    item = User.objects.get(pk=id)
    item.delete()

from discourseAdmin.models import dGroup
from discourseAdmin.forms import GroupForm
@login_required
def group_list(request, template='group/list.html'):
    d = {}
    d['group_list'] = dGroup.objects.all()
    return render(request, template, d)

def group_create(request, template='group/create.html'):
    d = {}
    d['form'] = GroupForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            item = form.save()
            #print(item)
            client = Utils.getDiscourseClient()
            try:
                groupDict = client.create_group(name=item.name)
            except:
                item.delete()
                messages.error(request, 'Discourse Fehler: Der Gruppenname entspricht nicht den Anforderungen. ')
                messages.error(request, sys.exc_info()[1])
                print("Error:", sys.exc_info()[0])
            else:
                item.discourse_group_id = groupDict['basic_group']['id']
                item.save()
                print(groupDict)
                return redirect('group-list')
        else:
            d['form'] = form
            messages.error(request, 'Es ist eine Fehler im Formular aufgetreten ')
    return render(request, template, d)

from discourseAdmin.forms import GroupForm
@login_required
def group_details(request, id, template='group/details.html'):
    d = {}
    item = get_object_or_404(dGroup, pk=id)
    #print(dGroup.objects.filter(id=1).all())
    d['members'] = item.members.all()
    
    d['form'] = GroupForm(instance=item)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            return JsonResponse(data={'form': GroupForm(instance=item).as_p(), 'token': get_token(request)})
        else:
            d['form'] = form
            return JsonResponse(data={'form': d['form'].as_p(), 'token': get_token(request)}, success=False)
    d['group'] = dGroup.objects.get(pk=id)
    return render(request, template, d)

@login_required
def group_delete(request, id):
    item = dGroup.objects.get(pk=id)
    item.delete()
    return JsonResponse()

from discourseAdmin.models import User_Groups
@login_required
def activate_user(request, user_id):
    #TODO: check authorisation ? Nö darf jede aus dem Staff
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    print(user.__dict__)
    
    # soll auch passieren damit man auch in discourse sieht wer deaktiviert ist
    # TODO: lieber discourse_user (das ist ne id) nehmen? dann aber daten overhead ?
    try:
        client = Utils.getDiscourseClient()
        dUser = client.user(username=user.username)
        print(dUser['id'])
    except: print ("Der Benutzer "+user.username+" scheint nicht sinvoll mit discourse verknüpft zu sein")
    try: client.activate(dUser['id'])
    except: print("scheinbar bereits aktiviert")
    try: client.unsuspend(dUser['id'])
    except: print("scheinbar nicht gesperrt")

    return redirect('user-list')

@login_required
def deactivate_user(request, user_id):
    #TODO: check authorisation ? Nö darf jede aus dem Staff
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()

    try:
        client = Utils.getDiscourseClient()
        dUser = client.user(username=user.username)
        client.deactivate(dUser['id'])
        client.suspend(dUser['id'],365000,"Gesperrt von user "+request.user.username)
    except: print ("Der Benutzer "+user.username+" scheint nicht sinvoll mit discourse verknüpft zu sein")
    try: client.deactivate(dUser['id'])
    except: print("scheinbar nicht aktiviert")
    try:         client.suspend(dUser['id'],365000,"Gesperrt von user "+request.user.username)
    except: print("scheinbar bereits gesperrt")

    return redirect('user-list')


@login_required
def add_user_to_group(request, user_id, group_id):
    if User_Groups.isGroupAdmin(user_id=request.user.id, group_id = group_id) : 
        ug, create = User_Groups.objects.get_or_create(user_id=user_id, group_id = group_id)
        client = Utils.getDiscourseClient()
        client.add_user_to_group(ug.group.discourse_group_id,ug.user.participant.discourse_user)

    return redirect('user-details', id=user_id)

@login_required
def delete_user_from_group(request, user_id, group_id):
    if User_Groups.isGroupAdmin(user_id=request.user.id, group_id = group_id) : 
        ug = User_Groups.objects. get(user_id=user_id, group_id = group_id)
        ug.delete()
        client = Utils.getDiscourseClient()
        client.delete_group_member(ug.group.discourse_group_id,ug.user.participant.discourse_user)

    return redirect('user-details', id=user_id)

@login_required    
def user_groups_delete(request, id):
    item = User_Groups.objects.get(pk=id)
    item.delete()
    return JsonResponse()

from django.core.serializers.json import DjangoJSONEncoder
@login_required
#import_dgroups aktualisiert von discourse -> discourseAdmin (bitte vorsichtig verwenden)    
def import_dgroups(request):
    client = Utils.getDiscourseClient()
    groupsDict = client.groups()
    for groupDict in groupsDict:
        # gruppe in da erzeugen falls noch nicht vorhanden
        groupObj, created = dGroup.objects.get_or_create(discourse_group_id=groupDict['id'])
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

def import_dgroup(request, groupname, da_group_id):
    limit = request.GET.get("limit") if request.GET.get("limit") else 1000
    offset = request.GET.get("offset") if request.GET.get("offset") else 0
    client = Utils.getDiscourseClient()
    Utils.import_dgroup_members(groupname, da_group_id, limit, offset)
    return JsonResponse()

@login_required    
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

def change_password(request, template='user/change_password.html'):
    d = {}
    d['form'] = ChangePasswordForm()
    d['sso_links'] = sso_links
    d['ignore_sso_link'] = 'change_password' 
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if request.POST['new_password'] == request.POST['repeat_new_password']:
                user = User.objects.get(username=request.POST['username'])
                try:
                    password_validation.validate_password(request.POST['new_password'])
                except ValidationError as errs:
                    messages.error(request, 'Das hat nicht geklappt: Folgende Fehler sind aufgetreten:')
                    for err in errs:
                        messages.error(request, err)                
                else:
                    user.set_password(request.POST['new_password'])
                    user.save()
                    print(user)
                    messages.success(request, 'Password wurde erfolgreich geändert ')
            else:
                messages.error(request, 'Fehler: Deine neuen Passwörter stimmen nicht überein.')
                print(form);
        else:
            messages.error(request, 'Fehler: Deine Zugangsdaten sind falsch. Entweder exitiert der Benutzer nicht oder das Passwort ist falsch.')
            
    return render(request, template, d)

    
def create_user(request, template='user/create.html'):
    client = Utils.getDiscourseClient()
    d = {}
    d['sso_links'] = sso_links
    d['form'] = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                password_validation.validate_password(request.POST['password'])
            except ValidationError as errs:
                messages.error(request, 'Das hat nicht geklappt: Folgende Fehler sind aufgetreten:')
                for err in errs:
                    messages.error(request, err)
            else:
                item = form.save()
                item.set_password(item.password)
                Utils.create_discourse_user(item)
                messages.success(request, 'Dein Account wurde erfolgreich angelegt. Er muss nun freigeschaltet werden. Dann kannst du dich einloggen.')
            #return redirect('http://localhost:3000')
        else:
            messages.error(request, 'Das hat nicht geklappt. Dein Account wurde nicht angelegt.')
            d['form'] = form
            return render(request, template, d)
            #return JsonResponse(data={'form': d['form'].as_p(), 'token': get_token(request)}, success=False)
    d['user_list'] = User.objects.all()
    return render(request, template, d)
    #return JsonResponse()

from django.contrib.auth import authenticate
from gydiscourse.pydiscourse import sso
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def discourse_sso(request, template='user/login.html'):
    print("discourse_sso")

    d = {}
    d['sso_links'] = sso_links
    if hasattr(settings, 'FORCE_DISCOURSE_ADMIN_URL') : d['force_url'] = settings.FORCE_DISCOURSE_ADMIN_URL    
    else : d['force_url'] = False
    #sso und sig per get oder post auslesen
    d["sso"] = payload = request.GET.get('sso')
    #if d["sso"] == None : d["sso"] = payload = request.POST['sso']
    d["sig"] = signature = request.GET.get('sig')
    #if d["sig"] == None : d["sig"] = signature = request.POST['sig']
 
    #wenn kein sso vorhanden zurück zum sso client leiten
    if d["sso"] == None :
        return redirect(settings.DISCOURSE_BASE_URL)
    
    d['form'] = LoginForm()
    if request.method == 'POST':
        print("post anfrage")
        #print(request.POST['username'])
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
 
        # checken ob stattdessen ein Php Benutzer besteht
        if user is None:
            print("User is not authenticated by python try php")
            if Utils.isValidPhpUser(username=request.POST['username'], password=request.POST['password']):
                user = Utils.migrateUser(username=request.POST['username'], password=request.POST['password'])
        
        # wenn Benutzer valide sso validierung mit gruppen ausliefern  
        if user is not None:
            print("User ist vorhanden")
            Utils.watchImportantTopic(request, user.username)
            #print(user.__dict__)
            #groups = user.dgroup_set.all()
            #groupstr = ', '.join(map(str, list(groups)))
#             if hasattr(settings, 'DISCOURSE_INTERN_SSO_EMAIL') :
#                  user.email = '%s@%s' % (user.id, settings.DISCOURSE_INTERN_SSO_EMAIL) 
            print(user.__dict__)
            nonce = sso.sso_validate(payload, signature, settings.DISCOURSE_SSO_KEY)
            url = sso.sso_redirect_url(nonce, settings.DISCOURSE_SSO_KEY, user.email, user.participant.id, user.username) #, add_groups=groupstr, groups=groupstr)
            return redirect(settings.DISCOURSE_BASE_URL + url)
        else:
            messages.error(request, 'Das hat nicht geklappt: Benutzername oder Passwort ist falsch oder dein Account ist nicht freigeschaltet.')
    else:
        print("get anfrage")
    return render(request, template, d)
    #return redirect('http://discuss.example.com' + url)

@csrf_exempt
def testpd(request):
    #client = Utils.getDiscourseClient()
    #client.groups()
    #result = client.watch_topic(57, username="heiner", notification_level=3)
    #print(result)
    print(request.method)
    print(request)
    return JsonResponse()

@csrf_exempt
def testisvaliduser(request, template='user/tivu.html'):
    print("testisvaliduser")
    d =  {}
    d['form'] = LoginForm()
    if request.method == 'POST':
        print(request.POST['username'])
        try:
            password_validation.validate_password(request.POST['password'])
        except ValidationError as errs:
            messages.error(request, 'Das hat nicht geklappt: Folgende Fehler sind aufgetreten:')
            for err in errs:
                messages.error(request, err)                
                print(err)
        else:
            print("has a good password")
        
        print("and is a validPhpUser :")
        print(Utils.isValidPhpUser(username=request.POST['username'], password=request.POST['password']))
        print("_______")
    return render(request, template, d)
