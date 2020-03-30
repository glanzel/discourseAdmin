import pdb, json
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.core import serializers


# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.middleware.csrf import get_token
from django3scaffold.http import JsonResponse
from discourseAdmin.models import User
from discourseAdmin.forms import UserForm
from doctest import DebugRunner

def user_list(request, template='user/list.html'):
    d = {}
    d['form'] = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            item = form.save()
            return JsonResponse(data={'id': item.id, 'name': str(item), 'form': UserForm().as_p(), 'token': get_token(request)})
        else:
            d['form'] = form
            return JsonResponse(data={'form': d['form'].as_p(), 'token': get_token(request)}, success=False)
    d['user_list'] = User.objects.all()
    return render(request, template, d)

from discourseAdmin.forms import UserForm
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
def user_details(request, id, template='user/details.html'):
    d = {}
    item = get_object_or_404(User, pk=id)
    #print(serializers.serialize('json', [ item, ]))
    #print(item.dgroup_set.all())
    
    groups = dGroup.objects.all().filter(user_groups__rights=1)

    #print(groups) 
    d['form'] = HasDiscoGroups()
    
    #return render(request, template, d)
    #d['form'] = HasDiscoGroups([(1,2)])
    
    #print(d['form']) 
    
    if request.method == 'POST':
        print(request.POST)
        form = HasDiscoGroups(request.POST, instance=item)
        print(serializers.serialize('json', [ item, ]))
        if form.is_valid():
            print(form.cleaned_data)
            item = form.save()
            #print(item)
            #form.save_m2m()
            return JsonResponse(data={'form': UserForm(instance=item).as_p(), 'token': get_token(request)})
        else:
            d['form'] = form
            return JsonResponse(data={'form': d['form'].as_p(), 'token': get_token(request)}, success=False)
    d['user'] = User.objects.get(pk=id)
    return render(request, template, d)



def user_delete(request, id):
    item = User.objects.get(pk=id)
    item.delete()
    return JsonResponse()

from discourseAdmin.models import dGroup
from discourseAdmin.forms import GroupForm
def group_list(request, template='group/list.html'):
    d = {}
    d['form'] = GroupForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            item = form.save()
            return JsonResponse(data={'id': item.id, 'name': str(item), 'form': GroupForm().as_p(), 'token': get_token(request)})
        else:
            d['form'] = form
            return JsonResponse(data={'form': d['form'].as_p(), 'token': get_token(request)}, success=False)
    d['group_list'] = dGroup.objects.all()
    return render(request, template, d)

from discourseAdmin.forms import GroupForm
def group_details(request, id, template='group/details.html'):
    d = {}
    item = get_object_or_404(dGroup, pk=id)
    #print(dGroup.objects.filter(id=1).all())
    
    
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

def group_delete(request, id):
    item = dGroup.objects.get(pk=id)
    item.delete()
    return JsonResponse()

from discourseAdmin.models import User_Groups
from discourseAdmin.forms import User_GroupsForm
def user_groups_list(request, template='user_groups/list.html'):
    d = {}
    d['form'] = User_GroupsForm()
    if request.method == 'POST':
        form = User_GroupsForm(request.POST)
        if form.is_valid():
            item = form.save()
            return JsonResponse(data={'id': item.id, 'name': str(item), 'form': User_GroupForm().as_p(), 'token': get_token(request)})
        else:
            d['form'] = form
            return JsonResponse(data={'form': d['form'].as_p(), 'token': get_token(request)}, success=False)
    d['user_groups_list'] = User_Groups.objects.all()
    return render(request, template, d)

from discourseAdmin.forms import User_GroupsForm
def user_groups_details(request, id, template='user_groups/details.html'):
    d = {}
    item = get_object_or_404(User_Groups, pk=id)
    d['form'] = User_GroupForm(instance=item)
    if request.method == 'POST':
        form = User_GroupForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            return JsonResponse(data={'form': User_GroupForm(instance=item).as_p(), 'token': get_token(request)})
        else:
            d['form'] = form
            return JsonResponse(data={'form': d['form'].as_p(), 'token': get_token(request)}, success=False)
    d['user_groups'] = User_Groups.objects.get(pk=id)
    return render(request, template, d)

def user_groups_delete(request, id):
    item = User_Groups.objects.get(pk=id)
    item.delete()
    return JsonResponse()


from pydiscourse import DiscourseClient
from django.core.serializers.json import DjangoJSONEncoder
def import_dgroups(request):
    client = DiscourseClient(
        'http://localhost:3000',
        api_username='system',
        api_key='84531905176dfd5d7cde45008430f879da00e43a94510cd39d540bd13d1d01b1')
    groupsDict = client.groups()
    for groupDict in groupsDict:
        print(groupDict)
        print("-");
        
        group = dGroup();
        for key in groupDict:
            setattr(group, key, groupDict[key])
            #print(groupDict[key]) 
        #groups.append(json.loads(groupJson))
        print(group.__dict__)
        print("-");
        group.save();
    return JsonResponse()
    #return JsonResponse(groupsDict, DjangoJSONEncoder,False) #warum geht das nicht es sollte korrekt sein

from pydiscourse import DiscourseClient
def import_users(request):
    client = DiscourseClient(
        'http://localhost:3000',
        api_username='system',
        api_key='84531905176dfd5d7cde45008430f879da00e43a94510cd39d540bd13d1d01b1')
    usersDict = client.users()
    for userDict in usersDict:
        print(userDict)
        print("-");
        
        user = User();
        for key in userDict:
            setattr(user, key, userDict[key])
        print(user.__dict__)
        print("-");
        #user.save();
    return JsonResponse()
    #return JsonResponse(usersDict, DjangoJSONEncoder,False) #warum geht das nicht es sollte korrekt sein
    
from pydiscourse import DiscourseClient
def create_user(request, template='user/create.html'):
    client = DiscourseClient(
        'http://localhost:3000',
        api_username='system',
        api_key='84531905176dfd5d7cde45008430f879da00e43a94510cd39d540bd13d1d01b1')
    d = {}
    d['form'] = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            item = form.save()
            #print(item.__dict__)
            email = item.username + "@bekanntedomain.de"
            dUser = client.create_user(item.first_name, item.username, email, item.password, active='true')
            client.deactivate(dUser['user_id'])
            client.activate(dUser['user_id'])
            return JsonResponse(data={'id': item.id, 'name': str(item), 'form': UserForm().as_p(), 'token': get_token(request)})
        else:
            d['form'] = form
            return JsonResponse(data={'form': d['form'].as_p(), 'token': get_token(request)}, success=False)
    d['user_list'] = User.objects.all()
    return render(request, template, d)
    #return JsonResponse()
    
