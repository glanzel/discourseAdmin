from django import forms
from discourseAdmin.models import User
from discourseAdmin.models import dGroup

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        #fields = "__all__"
        fields = ('username', 'password');
    #password = forms.CharField(widget=forms.PasswordInput)
    #dgroup_set = forms.ModelMultipleChoiceField(queryset=dGroup.objects.all().filter(user_groups__rights=1), widget = forms.CheckboxSelectMultiple)
    #users_permissons = ""

class DetailUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password');
    #password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username','pattern':'[A-Za-z0-9_]+', 'title':'Nur Buchstaben, Ziffern und Unterstrich ist erlaubt'}), min_length=3, max_length=20)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}),min_length=8)


class ChangePasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password');
    #password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username','pattern':'[A-Za-z0-9_]+', 'title':'Nur Buchstaben, Ziffern und Unterstrich ist erlaubt'}), min_length=3, max_length=20)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}),min_length=8)
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'new password'}),min_length=8)
    repeat_new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'repeat new password'}),min_length=8)


class GroupForm(forms.ModelForm):
    class Meta:
        model = dGroup
        #fields = "__all__"
        fields = ('name', 'description')
    name = forms.CharField(widget=forms.TextInput(attrs={'pattern':'[A-Za-z0-9_-.]+', 'title':'Nur Buchstaben, Ziffern, Leerzeichen  und _-. erlaubt'}), min_length=3)
    #members = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget = forms.CheckboxSelectMultiple)


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
