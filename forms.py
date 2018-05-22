from django import forms
from .models import *
from django.forms import ModelForm

class NewItemForm(ModelForm):
    class Meta:
        model= Item
        fields= ['name', 'attributed_to' ]
        labels = {
        'name': 'Contenu',
        'attributed_to': 'Attribué à',
    }
    def __init__(self, theme, *args, **kwargs):
        super(NewItemForm, self).__init__(*args, **kwargs)
        self.fields['attributed_to'].queryset = theme.authorized_user.all()

class NewItemCommentForm(ModelForm):
    class Meta:
        model= ItemComment
        fields= ['name', ]
        labels = {
        'name': 'Commentaire',
    }

class NewSubThemeForm(ModelForm):
    class Meta:
        model= SubTheme
        fields= ['name', ]
        labels = {
        'name': 'Titre',
    }