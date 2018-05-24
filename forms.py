from django import forms
from .models import *
from django.forms import ModelForm

class NewItemForm(ModelForm):
    class Meta:
        model= Item
        fields= ['name']
        labels = {
        'name': 'Contenu',
        'attributed_to': 'Attribué à',
    }


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