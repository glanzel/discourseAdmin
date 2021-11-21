import pdb, json, sys
import logging
import datetime

from django.core import serializers #benutzen wir das ?
from django.core.exceptions import ValidationError
from django.conf import settings

#from django.contrib import auth
from django.contrib.auth import password_validation
from django.contrib.auth import authenticate
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

sso_links = {'anmeldung':'Login:Discourse', 'create_user':'Registrieren', 'change_password':'Passwort ändern', 'login':'Login:Adminbereich'}

logger = logging.getLogger(__name__)

@login_required
def staff_list(request, title='OG Admin Liste', template='user/list.html'):
    d = {}
    d['title'] = title
    d['user_list'] = User.objects.all().filter(is_staff=True).order_by('participant__department_id', 'username')
    return render(request, template, d)


@login_required
def user_list(request, title='Benutzerliste', template='user/list.html'):
    d = {}
    d['title'] = title
    #logger.debug("this is user-list")

    d['user_list'] = User.objects.all().order_by('-date_joined', '-last_login')
    tmp_admin_groups = User_Groups.objects.filter(user_id=request.user.id, rights = 1)
    admin_groups = []
    for ag in tmp_admin_groups: 
        admin_groups.append(ag.group_id)
    d['is_group_admin'] = admin_groups
    #print(d['is_group_admin'])
    if request.method == 'GET':
        filters = {}
        for key in request.GET:
            if request.GET[key] == 'True': filters[key] = True
            if request.GET[key] == 'False': filters[key] = False
            if key == 'department' : filters['participant__department_id'] = request.GET[key]    
        d['user_list'] = d['user_list'].filter(**filters)
    return render(request, template, d)



from discourseAdmin.forms import UserForm
@staff_member_required
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
@staff_member_required
def user_details(request, id, template='user/details.html'):
    d = {}
    user = item = get_object_or_404(User, pk=id)
    d['user_groups'] = item.dgroup_set.all()
    d['admin_groups'] = dGroup.objects.all().filter(user_groups__rights=1, user_groups__user_id=request.user.id).exclude(id__in=d['user_groups'])

    if request.user.is_superuser : 
        d['all_groups'] = dGroup.objects.all()
    else:
        d['all_groups'] = False
        
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
    d['other_user'] = User.objects.get(pk=id)
    
    # check connection to discourse
    client = Utils.getDiscourseClient()
    try: 
        p = user.participant
        dUserDetails = client.user_all(user_id=p.discourse_user)
    except: 
        d['dUser_exists'] = False
    else:
        d['dUser_exists'] = True
        
    return render(request, template, d)

@staff_member_required
def user_delete(request, id):
    #TODO: wieder einbauen ?
    return JsonResponse()
    item = User.objects.get(pk=id)
    item.delete()

def change_password(request, template='user/change_password.html'):
    d = {}
    d['form'] = ChangePasswordForm()
    d['sso_links'] = sso_links
    d['ignore_sso_link'] = 'change_password' 
    d['theuser'] = request.user
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                logger.info("User "+request.POST['username']+" kann Passwort nicht ändern:  Entweder exitiert der Benutzer nicht oder das alte Passwort ist falsch")
                messages.error(request, 'Fehler: Deine Zugangsdaten sind falsch. Entweder exitiert der Benutzer nicht oder das alte Passwort ist falsch.')
                return render(request, template, d)
        else: user = request.user
 
        Utils.change_password(request, user, request.POST['new_password'], request.POST['repeat_new_password'])
    return render(request, template, d)

def change_user_password(request, user_id, template='user/change_user_password.html'):
    d = {}
    d['form'] = ChangePasswordForm()
    d['sso_links'] = sso_links
    d['ignore_sso_link'] = 'change_password' 
    d['user_id'] = user_id;
    d['theuser'] = other_user = User.objects.get(id=user_id)
    
    print("theotheruser")
    print(other_user)
    print(user_id)
     
    if request.method == 'POST':
        ou_dep = other_user.participant.department
        u_dep = request.user.participant.department
        if ( request.user.is_staff and ((ou_dep is None) or (u_dep == ou_dep)) or request.user.is_superuser) :
            Utils.change_password(request, other_user, request.POST['new_password'], request.POST['repeat_new_password'])
        else:
            messages.error("keine Berechtigung")
            return redirect('user/'+other_user_id)

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
                basicgroup = Utils.get_or_create_basic_group()
                basicgroup.user_set.add(item)
                logger.info("User "+item.username+" wurde erfolgreich angelegt.")
                messages.success(request, 'Dein Account wurde erfolgreich angelegt. Er muss nun freigeschaltet werden. Dann kannst du dich einloggen.')
                return redirect('/')
        else:
            messages.error(request, 'Das hat nicht geklappt. Dein Account wurde nicht angelegt.')
            d['form'] = form
            return render(request, template, d)
            #return JsonResponse(data={'form': d['form'].as_p(), 'token': get_token(request)}, success=False)
    d['user_list'] = User.objects.all()
    return render(request, template, d)
    #return JsonResponse()

@staff_member_required
def create_discourse_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    try: p = user.participant
    except: logger.info("User "+user.username+" wird in discourse neu angelegt.  Er scheint vorher nicht dort existiert zu haben kein Participatn gefunden.")
    else: 
        client = Utils.getDiscourseClient()
        try: userDetails = client.user_all(user_id=p.discourse_user)
        except: 
            logger.info("User "+user.username+" wird wird in discourse neu angelegt.  Participant existierte zwar, er scheint aber trotzdem nicht in discourse zu existieren.")
            user.participant.delete()
        else:
            messages.error(request, "Der Benutzer "+user.username+" scheint doch zu existieren. (discourse.id:"+p.discourse_user+" da.id:"+ +" user_id) Die Verbindung zu Discourse besteht bereits, der Benutzer existiert auch dort. Es scheint eine anderer Fehler vorzuliegen. Wende dich bitte an einen Admin und poste diesen Text.")
            return redirect('user-details', id=user_id)
    Utils.create_discourse_user(user)
    basicgroup = Utils.get_or_create_basic_group()
    basicgroup.user_set.add(user)
    return redirect('user-details', id=user_id)

from discourseAdmin.models import User_Groups
@staff_member_required
def activate_user(request, user_id):
    #TODO: check authorisation ? Nö darf jede aus dem Staff
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.last_login = datetime.datetime.now()
    user.save()
    print(user.__dict__)
    
    # soll auch passieren damit man auch in discourse sieht wer deaktiviert ist
    # TODO: lieber discourse_user (das ist ne id) nehmen? dann aber daten overhead ?
    try:
        client = Utils.getDiscourseClient()
        p = user.participant
        dUser = client.user_all(user_id=p.discourse_user)

        print(dUser['id'])
    except: 
        messages.error(request, "Der Benutzer "+user.username+" scheint nicht sinvoll mit discourse verknüpft zu sein, ist jetzt nur im backend aktiviert")
        print ("Der Benutzer "+user.username+" scheint nicht sinvoll mit discourse verknüpft zu sein, ist jetzt nur im backend aktiviert")
        return redirect('user-list')
    
    try: client.activate(dUser['id'])
    except: 
        messages.error(request, "Der Benutzer "+user.username+" scheinbar bereits aktiviert ?.")
        print("scheinbar bereits aktiviert")
    try: client.unsuspend(dUser['id'])
    except: print("scheinbar nicht gesperrt")

    return redirect('user-list')

@staff_member_required
def deactivate_user(request, user_id, info=None):
    #TODO: check authorisation ? Nö darf jede aus dem Staff
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()

    try:
        client = Utils.getDiscourseClient()
        p = user.participant
        dUser = client.user_all(user_id=p.discourse_user)
    except: 
        messages.error(request, "Der Benutzer "+user.username+" scheint nicht sinvoll mit discourse verknüpft zu sein, ist jetzt nur im backend deaktiviert")
        print ("Der Benutzer "+user.username+" scheint nicht sinvoll mit discourse verknüpft zu sein")
    else:
        try: client.deactivate(dUser['id'])
        except: print("scheinbar nicht aktiviert")
        try:
            if info is None : info = "Gesperrt von user "+request.user.username
            client.suspend(dUser['id'],365000,info)
        except: print("scheinbar bereits gesperrt")
    return redirect('user-list')


@staff_member_required
def set_department(request, user_id, group_id):
    if (User_Groups.isGroupAdmin(user_id=request.user.id, group_id = group_id)) or request.user.is_superuser: 
        dgroup = dGroup.objects.get(id=group_id) 
        otheruser = User.objects.get(id=user_id)
        otheruser.participant.department = dgroup
        otheruser.participant.save()
    return redirect('user-details', id=user_id)


@staff_member_required
def unset_department(request, user_id):
    otheruser = User.objects.get(id=user_id)
    group_id = otheruser.participant.department.id
    if (User_Groups.isGroupAdmin(user_id=request.user.id, group_id = group_id)) or request.user.is_superuser: 
        otheruser.participant.department = None
        otheruser.participant.save()
    return redirect('user-details', id=user_id)

