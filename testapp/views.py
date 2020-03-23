from django.shortcuts import render
from generic_scaffold import CrudManager
from testapp.models import Post

def post_list(request):
    return render(request, 'testapp/post_list.html', {})
    

class PostCrudManager(CrudManager):
    model = Post
    prefix = 'cpost'

