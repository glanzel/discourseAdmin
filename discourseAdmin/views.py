import pdb, json
import logging
import datetime
from django.shortcuts import render
#from django.forms.models import model_to_dict
from django.core import serializers
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.middleware.csrf import get_token
from django3scaffold.http import JsonResponse
from discourseAdmin.models import Participant, User
from discourseAdmin.forms import UserForm, LoginForm
from discourseAdmin.logic import Utils
from doctest import DebugRunner
from django.conf import settings
from pip._vendor.colorama.ansi import Fore
#from lib2to3.pgen2.tokenize import group # wo kommt das her ?
#from __builtin__ import True # und was soll das  ?


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
    item = User.objects.get(pk=id)
    item.delete()
    return JsonResponse()

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
            groupDict = client.create_group(name=item.name)
            item.discourse_group_id = groupDict['basic_group']['id']
            item.save()
            print(groupDict)
            return redirect('group-list')
        else:
            d['form'] = form
            print(form)
            return JsonResponse(data={'form': d['form'].as_p(), 'token': get_token(request)}, success=False)
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
    
    # TODO: lieber discourse_user (das ist ne id) nehmen? dann aber daten overhead ?
    # ist dieser Teil wegen sso eventuell jetzt obsolete ? vermutlich.
    client = Utils.getDiscourseClient()
    dUser = client.user(username=user.username)
    print(dUser['id'])
    client.deactivate(dUser['id'])
    client.activate(dUser['id'])

    return redirect('user-list')

@login_required
def deactivate_user(request, user_id):
    #TODO: check authorisation ? Nö darf jede aus dem Staff
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    
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

from pydiscourse import DiscourseClient
from django.core.serializers.json import DjangoJSONEncoder
@login_required
#import_dgroups aktualisiert von discourse -> discourseAdmin (bitte vorsichtig verwenden)    
def import_dgroups(request):
    client = Utils.getDiscourseClient()
    groupsDict = client.groups()
    for groupDict in groupsDict:
        groupObj, created = dGroup.objects.get_or_create(discourse_group_id=groupDict['id'])
        print("import: "+str(groupDict['id'])+" : "+groupDict['name'])

        for key in groupDict:
            if key != "id":
                setattr(groupObj, key, groupDict[key])

        if created: 
            print("created")
            groupObj.create_date = datetime.datetime.now()
        else: 
            print("already exists") #TODO: Discourse group aktualisieren ?      
            groupObj.update_date = datetime.datetime.now()
        
        groupObj.discourse_group_id = groupDict['id']         
        groupObj.save();

        print("-");
        groupDetails = client.group(groupDict['name'])
        #print(groupDetails)
        for member in groupDetails['members']:
            p = Participant.objects.get(discourse_user=member['id'])
            ug, create = User_Groups.objects.get_or_create(user_id=p.user_id, group_id = groupObj.id)
            if created:
                ug.save()    
    
    return JsonResponse()
    #return JsonResponse(groupsDict, DjangoJSONEncoder,False) #warum geht das nicht es sollte korrekt sein

from pydiscourse import DiscourseClient
@login_required    
def import_users(request):
    client = Utils.getDiscourseClient()
    usersDict = client.users()
    for userDict in usersDict:
        userObj, created = User.objects.get_or_create(username=userDict['username'])

        #print(userObj.__dict__)
        #print(created)
        
        if created: 
            userDetails = client.user_all(user_id=userDict['id'])
            ssoDetails = userDetails['single_sign_on_record']         
            if ssoDetails != None :
                print(ssoDetails['external_email'])
                userObj.email = ssoDetails['external_email']

            for key in userDict:
                if key != "id":
                    setattr(userObj, key, userDict[key])

            userObj.save();

        else :
            #TODO overwrite Userdata in Discourse
            print("TODO")
        
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
    
from pydiscourse import DiscourseClient
def create_user(request, template='user/create.html'):
    client = Utils.getDiscourseClient()
    d = {}
    d['form'] = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            item = form.save()
            item.set_password(item.password)
            item.is_active = False
            if hasattr(settings, 'DISCOURSE_INTERN_SSO_EMAIL') :
                item.email = '%s%s@%s' % ("da", item.id, settings.DISCOURSE_INTERN_SSO_EMAIL)
                print(item.email)
            item.save()
            
            #der benutzer wird in discourse schon erzeugt damit gruppen etc, bereits gesetzt werden können. external_id kann aber erst beim sso login gesetzt werden    
            dUser = client.create_user(item.username, item.username, item.email, item.password, active='true')
            client.deactivate(dUser['user_id']), 
            p = Participant(user = item, discourse_user=dUser['user_id'])
            p.save()
            
            print("******************* item dict *****************")
            print(item.__dict__)
            print("******************* form dict *****************")
            print(form.__dict__)
            print("-----")
            return redirect('http://localhost:3000' + url)
        else:
            d['form'] = form
            return JsonResponse(data={'form': d['form'].as_p(), 'token': get_token(request)}, success=False)
    d['user_list'] = User.objects.all()
    return render(request, template, d)
    #return JsonResponse()

from django.contrib.auth import authenticate
from pydiscourse import sso
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def discourse_sso(request, template='user/login.html'):
    print("discourse_sso")
    #print(request.method)
    print(request)
    
    d = {}
    d["sso"] = payload = request.GET.get('sso')
    if d["sso"] == None : d["sso"] = payload = request.POST['sso']
    print(d["sso"])
    d["sig"] = signature = request.GET.get('sig')
    if d["sig"] == None : d["sig"] = signature = request.POST['sig']
    
    d['form'] = LoginForm()
    if request.method == 'POST':
        #print(request.POST['username'])
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
 
        # checken ob stattdessen ein Php Benutzer besteht
        if user is None:
            if Utils.isValidPhpUser(username=request.POST['username'], password=request.POST['password']):
                user = User.objects.filter(username=request.POST['username']).get()
                user.set_password(request.POST['password'])
                user.save()

        print(user)
        
        
        # wenn Benutzer valide sso validierung mit gruppen ausliefern  
        if user is not None:
            Utils.watchImportantTopic(request, user.username)
            nonce = sso.sso_validate(payload, signature, settings.DISCOURSE_SSO_KEY)
            #print(user.__dict__)
            groups = user.dgroup_set.all()
            groupstr = ', '.join(map(str, list(groups)))
#             if hasattr(settings, 'DISCOURSE_INTERN_SSO_EMAIL') :
#                  user.email = '%s@%s' % (user.id, settings.DISCOURSE_INTERN_SSO_EMAIL) 
            print(user.__dict__)
            url = sso.sso_redirect_url(nonce, settings.DISCOURSE_SSO_KEY, user.email, user.participant.id, user.username, add_groups=groupstr, groups=groupstr)
            return redirect(settings.DISCOURSE_BASE_URL + url)
        else:
            return redirect(settings.DISCOURSE_BASE_URL + "/login/?alert=zugangsdaten sind falsch")
    else:
        print("ahah")
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
