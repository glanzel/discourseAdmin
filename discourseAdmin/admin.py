from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from discourseAdmin.models import Participant,dGroup, User_Groups
from discourseAdmin.forms import User_GroupsForm, LoginForm
from cProfile import label
import easyaudit
from easyaudit import admin as ea_admin

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
class MyAdmin(BaseUserAdmin):
    #form = MyUserAdminForm
    #print(form)
    inlines = (UserGroupsInline, ParticipantInline)
    
    class Media:
        css = {
             'all': ('css/da_main.css',)
        }

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, MyAdmin)

from discourseAdmin.models import dGroup
admin.site.register(dGroup)


# "Admin" Seite für nörmale Benutzer
class UserAdminSite(AdminSite):
    #login_form = LoginForm
    def has_permission(self, request):
        return request.user.is_active

user_admin_site = UserAdminSite(name='usersadmin')
user_admin_site.index_template = 'base.html'
user_admin_site.register(User,MyAdmin)
if settings.DJANGO_EASY_AUDIT_ADMIN_SHOW_MODEL_EVENTS:
    user_admin_site.register(easyaudit.models.CRUDEvent, ea_admin.CRUDEventAdmin)
# Run user_admin_site.register() for each model we wish to register
# for our admin interface for users
