import pdb, json
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
from discourseAdmin.forms import UserForm
from discourseAdmin.logic import Utils
from doctest import DebugRunner


@login_required
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
    #print(serializers.serialize('json', [ item, ]))
    d['user_groups'] = item.dgroup_set.all()
    print(d['user_groups'])
    d['admin_groups'] = dGroup.objects.all().filter(user_groups__rights=1, user_groups__user_id=request.user.id).exclude(id__in=d['user_groups'])
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
@login_required
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

@login_required
def group_delete(request, id):
    item = dGroup.objects.get(pk=id)
    item.delete()
    return JsonResponse()

from discourseAdmin.models import User_Groups
@login_required
def add_user_to_group(request, user_id, group_id):
    #TODO: check authorisation
    ug, create = User_Groups.objects.get_or_create(user_id=user_id, group_id = group_id)
    return redirect('user-details', id=user_id)

@login_required
def delete_user_from_group(request, user_id, group_id):
    #TODO: check authorisation
    ug = User_Groups.objects. get(user_id=user_id, group_id = group_id)
    ug.delete()
    return redirect('user-details', id=user_id)

@login_required    
def user_groups_delete(request, id):
    item = User_Groups.objects.get(pk=id)
    item.delete()
    return JsonResponse()


from pydiscourse import DiscourseClient
from django.core.serializers.json import DjangoJSONEncoder
def import_dgroups(request):
    client = Utils.getDiscourseClient()
    groupsDict = client.groups()
    for groupDict in groupsDict:
        groupObj, created = dGroup.objects.get_or_create(id=groupDict['id'])
        if created: 
            print(groupDict)
            print("-");
            
            groupObj = dGroup();
            for key in groupDict:
                setattr(groupObj, key, groupDict[key])
                #print(groupDict[key]) 
            #groups.append(json.loads(groupJson))
            print(groupObj.__dict__)
            print("-");
            groupObj.save();
        else:
            print("TODO?")
            #TODO: Discourse group aktualisieren ?      
        groupDetails = client.group(groupDict['name'])
        print(groupDetails)
        for member in groupDetails['members']:
            p = Participant.objects.get(discourse_user=member['id'])
            ug, create = User_Groups.objects.get_or_create(user_id=p.user_id, group_id = groupObj.id)
            if created:
                ug.save()    
    
    return JsonResponse()
    #return JsonResponse(groupsDict, DjangoJSONEncoder,False) #warum geht das nicht es sollte korrekt sein

from pydiscourse import DiscourseClient
def import_users(request):
    client = Utils.getDiscourseClient()
    usersDict = client.users()
    for userDict in usersDict:
        userObj, created = User.objects.get_or_create(username=userDict['username'])
        #print(userObj.__dict__)
        #print(created)
        if created: 
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
            item.save()
            email = item.username + "@bekanntedomain.de"
            dUser = client.create_user(item.username, item.username, email, item.password, active='true')
            client.deactivate(dUser['user_id'])
            client.activate(dUser['user_id'])
            p = Participant(user = item, discourse_user=dUser['user_id'])
            p.save()
            
            #item.discourse_user_id = dUser['user_id']
            #form.discourse_user_id = dUser['user_id']
            #item.save()
            #form.save()
            print("******************* item dict *****************")
            print(item.__dict__)
            print("******************* form dict *****************")
            print(form.__dict__)
            print("-----")
            return JsonResponse(data={'id': item.id, 'name': str(item), 'form': UserForm().as_p(), 'token': get_token(request)})
        else:
            d['form'] = form
            return JsonResponse(data={'form': d['form'].as_p(), 'token': get_token(request)}, success=False)
    d['user_list'] = User.objects.all()
    return render(request, template, d)
    #return JsonResponse()
    
