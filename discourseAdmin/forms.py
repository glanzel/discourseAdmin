from django import forms
from discourseAdmin.models import User
from discourseAdmin.models import dGroup

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        #fields = "__all__"
        fields = ('username', 'is_active', 'password');
    password = forms.CharField(widget=forms.PasswordInput)
    #dgroup_set = forms.ModelMultipleChoiceField(queryset=dGroup.objects.all().filter(user_groups__rights=1), widget = forms.CheckboxSelectMultiple)
    #users_permissons = ""

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password');
    password = forms.CharField(widget=forms.PasswordInput)


class GroupForm(forms.ModelForm):
    class Meta:
        model = dGroup
        fields = "__all__"
    members = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget = forms.CheckboxSelectMultiple)


from discourseAdmin.models import User_Groups

class User_GroupsForm(forms.ModelForm):
    class Meta:
        model = User_Groups
        fields = "__all__"
        
        
# class HasDiscoGroups(forms.Form):
#     dgroup_set = forms.ModelMultipleChoiceField(queryset=dGroup.objects.all().filter(user_groups__rights=1), widget = forms.CheckboxSelectMultiple)
# #     def __init__(self, *args,**kwargs):
# #         super(HasDiscoGroups, self).__init__(*args,**kwargs)
# #         print(kwargs)
# #         mychoice = kwargs['queryset'] 
# #         self.fields['dgroup_set'] = forms.ModelMultipleChoiceField(queryset=mychoices, widget = forms.CheckboxSelectMultiple)
#     #groups = forms.MultipleChoiceField(choices=[(1,"2")])

class HasDiscoGroups(forms.ModelForm):
    class Meta:
        model = User
        fields = []
    dgroup_set = forms.ModelMultipleChoiceField(queryset=dGroup.objects.all().filter(user_groups__rights=1), widget = forms.CheckboxSelectMultiple)
