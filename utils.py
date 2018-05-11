# python3
# functions called to get world specific variables.
from .models import *
from .forms import *
from django.core.exceptions import ObjectDoesNotExist

'''
python3, meant to be executed in django shell
One shot order value attribution for subthemes
'''
from roadmap.models import Theme, subtheme

for theme in Theme.objects.all():
	counter = 1
	for subtheme in theme.subtheme_theme.all():
		subtheme.order = counter
		subtheme.save()
		counter += 1