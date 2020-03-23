from crudbuilder.abstract import BaseCrudBuilder
from testapp.models import Post

class PostCrud(BaseCrudBuilder):
        model = Post
        search_fields = ['title']
        tables2_fields = ('author', 'text')
        tables2_css_class = "table table-bordered table-condensed"
        tables2_pagination = 20  # default is 10
        login_required=True
        permission_required=True
        # permissions = {
        #   'list': 'example.person_list',
        #       'create': 'example.person_create'
        # }
