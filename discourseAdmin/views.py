import pdb, json, sys
import logging
import datetime

from django.core import serializers #benutzen wir das ?
from django.core.exceptions import ValidationError
from django.conf import settings

from django.contrib import auth
from django.contrib.auth import password_validation
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.middleware.csrf import get_token

from discourseAdmin.models import Participant, User, dGroup, User_Groups
from discourseAdmin.forms import UserForm, LoginForm, ChangePasswordForm, GroupForm
from discourseAdmin.logic import Utils

from django3scaffold.http import JsonResponse # TODO: wieder ausbauen zugunsten der std JsonResponse ?
from datetime import date
from _ast import If
from django.utils import safestring

#from doctest import DebugRunner #wird das benutzt ?
#from pip._vendor.colorama.ansi import Fore # was macht das ?
#from lib2to3.pgen2.tokenize import group # wo kommt das her ?
#from __builtin__ import True # und was soll das  ?

sso_links = {'anmeldung':'Login:Discourse', 'create_user':'Registrieren', 'change_password':'Passwort ändern', 'login':'Login:Adminbereich'}

logger = logging.getLogger(__name__)

@login_required
def group_list(request, template='group/list.html'):
    d = {}
    d['group_list'] = dGroup.objects.all()
    return render(request, template, d)

@staff_member_required
def group_create(request, template='group/create.html'):
    #TODO: ersteller ist automatisch groupadmin ?
    d = {}
    d['form'] = GroupForm()
    #print("group_create")
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            item = form.save()
            #print(item.__dict__)
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
                ug, create = User_Groups.objects.get_or_create(user_id=request.user.id, group_id = item.id)
                ug.rights = 1
                try: 
                    client.add_user_to_group(ug.group.discourse_group_id,ug.user.participant.discourse_user)
                except: 
                    ug.delete();
                    messages.error(request, 'Das hat nicht geklappt: Benutzer kann nicht zu dieser Gruppe hinzugefügt werden')
                print(groupDict)
                return redirect('group-list')
        else:
            d['form'] = form
            messages.error(request, 'Es ist eine Fehler im Formular aufgetreten ')
    return render(request, template, d)

from discourseAdmin.forms import GroupForm
@staff_member_required
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

@staff_member_required
def group_delete(request, id):
    item = dGroup.objects.get(pk=id)
    if item.members.count() < 2 or request.user.is_superuser: 
        client = Utils.getDiscourseClient()
        try:
            groupDict = client.delete_group(item.discourse_group_id)
        except:
            messages.error(request, item.name)
            messages.error(request, ' Discourse Fehler: Die Gruppe kann nicht gelöscht werden. ')
            messages.error(request, sys.exc_info()[1])
            print("Error:", sys.exc_info()[0])
        else:
            item.delete()
    return redirect('group-list')



@staff_member_required
def add_user_to_group(request, user_id, group_id):
    if (User_Groups.isGroupAdmin(user_id=request.user.id, group_id = group_id)) or request.user.is_superuser: 
        #messages.error(request, 'Alles okay')
        ug, create = User_Groups.objects.get_or_create(user_id=user_id, group_id = group_id)
        client = Utils.getDiscourseClient()
        try: client.add_user_to_group(ug.group.discourse_group_id,ug.user.participant.discourse_user)
        except Exception as err: 
            ug.delete();
            messages.error(request, safestring.mark_safe('Benutzer kann nicht zu dieser Gruppe hinzugefügt werden. Grund: <br> '+format(err)))
    return redirect('user-details', id=user_id)


@staff_member_required
def delete_user_from_group(request, user_id, group_id):
    if (User_Groups.isGroupAdmin(user_id=request.user.id, group_id = group_id)) or request.user.is_superuser : 
        ug = User_Groups.objects. get(user_id=user_id, group_id = group_id)
        client = Utils.getDiscourseClient()
        try: client.delete_group_member(ug.group.discourse_group_id,ug.user.participant.discourse_user)
        except Exception as err: messages.error(request, safestring.mark_safe('Benutzer kann nicht von dieser Gruppe gelöscht werden.  Grund: <br/> '+format(err)))
        else: ug.delete()

    return redirect('user-details', id=user_id)

@staff_member_required    
def user_groups_delete(request, id):
    item = User_Groups.objects.get(pk=id)
    item.delete()
    return JsonResponse()

def home(request, template='home.html'):
    d = {}
    d['sso_links'] = sso_links
    return render(request, template, d)

from django.contrib.auth import authenticate
from gydiscourse.pydiscourse import sso
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login(request, template='user/login.html'):
    d =  {}
    d['sso_links'] = sso_links
    d['form'] = LoginForm()
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None: 
            auth.login(request, user)        
            return redirect('staff-list')
            messages.info(request, 'Erfolgreich eingeloggt.')
        else:
            messages.error(request, 'Das hat nicht geklappt: Benutzername oder Passwort ist falsch oder dein Account ist nicht freigeschaltet.')
    return render(request, template, d)
        
@csrf_exempt
def logout(request):
    deactivate_inactives(request)
    auth.logout(request)        
    return redirect('/')

@csrf_exempt
def discourse_sso(request, template='user/sso_login.html'):
    #print("discourse_sso")

    d = {}
    d['sso_links'] = sso_links
    if hasattr(settings, 'FORCE_DISCOURSE_ADMIN_URL') : d['force_url'] = settings.FORCE_DISCOURSE_ADMIN_URL    
    else :  d['force_url'] = False
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
        #print("post anfrage")
        #print(request.POST['username'])
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
 
        # checken ob stattdessen ein Php Benutzer besteht
        if hasattr(settings, 'PHP_LOGIN_CHECK_URI'):
            if User.objects.filter(username=request.POST['username']).exists():  
                the_user = User.objects.get(username=request.POST['username'])
                last_login = the_user.last_login
            else:     
                last_login = None

            if last_login is None: #nur einmal migrieren
                if user is None:
                    logger.info("User "+request.POST['username']+" is not authenticated by python try php")
                    if Utils.isValidPhpUser(username=request.POST['username'], password=request.POST['password']):
                        user = Utils.migrateUser(username=request.POST['username'], password=request.POST['password'])
    
        # wenn Benutzer valide sso validierung mit gruppen ausliefern  
        if user is not None:
            #print("User ist vorhanden")
            user.last_login = datetime.datetime.now()
            user.save()
            Utils.watchImportantTopic(request, user.username)
            #print(user.__dict__)
            #groups = user.dgroup_set.all()
            #groupstr = ', '.join(map(str, list(groups)))
#             if hasattr(settings, 'DISCOURSE_INTERN_SSO_EMAIL') :
#                  user.email = '%s@%s' % (user.id, settings.DISCOURSE_INTERN_SSO_EMAIL) 
            #print(user.__dict__)
            nonce = sso.sso_validate(payload, signature, settings.DISCOURSE_SSO_KEY)
            url = sso.sso_redirect_url(nonce, settings.DISCOURSE_SSO_KEY, user.email, user.participant.id, user.username) #, add_groups=groupstr, groups=groupstr)
            return redirect(settings.DISCOURSE_BASE_URL + url)
        else:
            messages.error(request, 'Das hat nicht geklappt: Benutzername oder Passwort ist falsch oder dein Account ist nicht freigeschaltet.')
    else:
        print("get anfrage")
    return render(request, template, d)
    #return redirect('http://discuss.example.com' + url)

# deaktiviert bei logout automatisch inaktive benutzer wenn settings.DEACTIVATE_INACTIVE_AFTER_DAYS gesetz ist
# sonst passiert gar nichts
# kann von cronjob aufgerufen werden
di_logger = logging.getLogger('views.deactivate_inactive')
def deactivate_inactives(request):
    if(hasattr(settings, 'DEACTIVATE_INACTIVE_AFTER_DAYS')):
        logger.info("check deactivate_inactive")
        heute = datetime.datetime.now()
        tag_x = heute - datetime.timedelta(days=settings.DEACTIVATE_INACTIVE_AFTER_DAYS)
        users = User.objects.all().filter(date_joined__lte = tag_x, is_active=True).filter(Q(last_login__lte = tag_x) | Q(last_login = None));
        for user in users:
            #hier wird deaktiviert.
            di_logger.info("deaktiviere "+user.username+" wegen inaktivität")
            deactivate_user(request,user.id, "Automatisch gesperrt wegen Inaktivität ("+ str(settings.DEACTIVATE_INACTIVE_AFTER_DAYS)+ " Tage)")
    return JsonResponse()

# migration methode only
@staff_member_required    
def set_basic_group(request):
    basicgroup = Utils.get_or_create_basic_group()
    print(basicgroup);
    users = User.objects.all().exclude(groups__id=1)
    print(users);
    for user in users:
        basicgroup.user_set.add(user)
    return JsonResponse()
        

@csrf_exempt
def testpd(request):
    client = Utils.getDiscourseClient()
    #client.groups()
    #result = client.watch_topic(57, username="heiner", notification_level=3)
    result = client.watch_category(5, "heiner")
    print(result)
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


