from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.middleware.csrf import get_token
from django3scaffold.http import JsonResponse
from forum.models import Forum
from forum.forms import ForumForm

def forum_list(request, template='forum/list.html'):
    d = {}
    d['form'] = ForumForm()
    if request.method == 'POST':
        form = ForumForm(request.POST)
        if form.is_valid():
            item = form.save()
            return JsonResponse(data={'id': item.id, 'name': str(item), 'form': ForumForm().as_p(), 'token': get_token(request)})
        else:
            d['form'] = form
            return JsonResponse(data={'form': d['form'].as_p(), 'token': get_token(request)}, success=False)
    d['forum_list'] = Forum.objects.all()
    return render(request, template, d)

from forum.forms import ForumForm
def forum_details(request, id, template='forum/details.html'):
    d = {}
    item = get_object_or_404(Forum, pk=id)
    d['form'] = ForumForm(instance=item)
    if request.method == 'POST':
        form = ForumForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            return JsonResponse(data={'form': ForumForm(instance=item).as_p(), 'token': get_token(request)})
        else:
            d['form'] = form
            return JsonResponse(data={'form': d['form'].as_p(), 'token': get_token(request)}, success=False)
    d['forum'] = Forum.objects.get(pk=id)
    return render(request, template, d)

def forum_delete(request, id):
    item = Forum.objects.get(pk=id)
    item.delete()
    return JsonResponse()
