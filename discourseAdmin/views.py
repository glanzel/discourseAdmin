from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.middleware.csrf import get_token
from django3scaffold.http import JsonResponse
from discourseAdmin.models import User
from discourseAdmin.forms import UserForm

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
    groups = Group.objects.all().filter(user_groups__rights=1)
    print(groups) 
    d['form'] = HasDiscoGroups(groups)
    return render(request, template, d)
    #d['form'] = HasDiscoGroups([(1,2)])
    
    print(d['form']) 
    
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



def user_delete(request, id):
    item = User.objects.get(pk=id)
    item.delete()
    return JsonResponse()

from discourseAdmin.models import Group
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
    d['group_list'] = Group.objects.all()
    return render(request, template, d)

from discourseAdmin.forms import GroupForm
def group_details(request, id, template='group/details.html'):
    d = {}
    item = get_object_or_404(Group, pk=id)
    d['form'] = GroupForm(instance=item)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            return JsonResponse(data={'form': GroupForm(instance=item).as_p(), 'token': get_token(request)})
        else:
            d['form'] = form
            return JsonResponse(data={'form': d['form'].as_p(), 'token': get_token(request)}, success=False)
    d['group'] = Group.objects.get(pk=id)
    return render(request, template, d)

def group_delete(request, id):
    item = Group.objects.get(pk=id)
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
