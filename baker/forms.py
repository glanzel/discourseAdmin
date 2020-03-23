from django import forms
from .models import Bread, Cake


class BreadForm(forms.ModelForm):

    class Meta:
        model = Bread
        fields = ['title', 'text', 'description', 'geschnitten', 'created_date', 'published_date']
        exclude = []
        widgets = None
        localized_fields = None
        labels = {}
        help_texts = {}
        error_messages = {}

    def __init__(self, *args, **kwargs):
        return super(BreadForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        return super(BreadForm, self).is_valid()

    def full_clean(self):
        return super(BreadForm, self).full_clean()

    def clean_title(self):
        title = self.cleaned_data.get("title", None)
        return title

    def clean_text(self):
        text = self.cleaned_data.get("text", None)
        return text

    def clean_description(self):
        description = self.cleaned_data.get("description", None)
        return description

    def clean_geschnitten(self):
        geschnitten = self.cleaned_data.get("geschnitten", None)
        return geschnitten

    def clean_created_date(self):
        created_date = self.cleaned_data.get("created_date", None)
        return created_date

    def clean_published_date(self):
        published_date = self.cleaned_data.get("published_date", None)
        return published_date

    def clean(self):
        return super(BreadForm, self).clean()

    def validate_unique(self):
        return super(BreadForm, self).validate_unique()

    def save(self, commit=True):
        return super(BreadForm, self).save(commit)


class CakeForm(forms.ModelForm):

    class Meta:
        model = Cake
        fields = ['title', 'text', 'fruits', 'geschnitten', 'created_date', 'published_date']
        exclude = []
        widgets = None
        localized_fields = None
        labels = {}
        help_texts = {}
        error_messages = {}

    def __init__(self, *args, **kwargs):
        return super(CakeForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        return super(CakeForm, self).is_valid()

    def full_clean(self):
        return super(CakeForm, self).full_clean()

    def clean_title(self):
        title = self.cleaned_data.get("title", None)
        return title

    def clean_text(self):
        text = self.cleaned_data.get("text", None)
        return text

    def clean_fruits(self):
        fruits = self.cleaned_data.get("fruits", None)
        return fruits

    def clean_geschnitten(self):
        geschnitten = self.cleaned_data.get("geschnitten", None)
        return geschnitten

    def clean_created_date(self):
        created_date = self.cleaned_data.get("created_date", None)
        return created_date

    def clean_published_date(self):
        published_date = self.cleaned_data.get("published_date", None)
        return published_date

    def clean(self):
        return super(CakeForm, self).clean()

    def validate_unique(self):
        return super(CakeForm, self).validate_unique()

    def save(self, commit=True):
        return super(CakeForm, self).save(commit)

