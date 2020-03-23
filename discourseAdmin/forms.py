from django import forms


from discourseAdmin.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


from discourseAdmin.models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "__all__"


from discourseAdmin.models import User_Groups

class User_GroupsForm(forms.ModelForm):
    class Meta:
        model = User_Groups
        fields = "__all__"
        
class HasDiscoGroups(forms.Form):
    def __init__(self, mychoices, *args,**kwargs):
        super(HasDiscoGroups, self).__init__(*args,**kwargs) 
        self.fields['groups'] = forms.ModelMultipleChoiceField(mychoices)
    #groups = forms.MultipleChoiceField(choices=[(1,"2")])
