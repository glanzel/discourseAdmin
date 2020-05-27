from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from discourseAdmin.models import Participant,dGroup, User_Groups
from discourseAdmin.forms import User_GroupsForm
from cProfile import label


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ParticipantInline(admin.StackedInline):
    model = Participant
    can_delete = False
    verbose_name_plural = 'Participants'

class UserGroupsInline(admin.StackedInline):
    model = User_Groups
    can_delete = False
    verbose_name_plural = 'User_Groups'
    form = User_GroupsForm

# TODO: warum wird das nicht genommen ?
class MyUserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)
        #exclude = ('user_permission','group', 'date_joined') 

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    #form = MyUserAdminForm
    #print(form)
    inlines = (UserGroupsInline,)
    
    class Media:
        css = {
             'all': ('css/da_main.css',)
        }

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)


from discourseAdmin.models import dGroup
admin.site.register(dGroup)
