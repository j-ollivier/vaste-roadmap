from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

@login_required
#####################################################################
def Home(request):
    '''
        If user is authenticated, he can access the page. If he has
        accessible themes, he can see the one where his access is 
        granted.
    '''
    themes = Theme.objects.filter(
            authorized_user = request.user).order_by(
            'name')
    context = {
        'page_title': 'Themes',
        'themes': themes,
        'page_title' : 'Feuilles de route',
    }
    template = loader.get_template('roadmap/home.html')
    return HttpResponse(template.render(context, request))

@login_required
#####################################################################
def ThemeView(request, theme_uid):
    '''
        Display the content of the folder linked to the Galery object
    '''
    theme = Theme.objects.get(pk = theme_uid)
    if request.user in theme.authorized_user.all():
        context = {
            'theme': theme,
            'new_sub_theme_form' : NewSubThemeForm(),
            'subthemes': SubTheme.objects.filter(
                theme = theme).order_by('order').select_related(),
            'page_title' : theme.name,
        }
        template = loader.get_template('roadmap/theme_view.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect(
                '/nope')

@login_required
#####################################################################
def AddItem(request, subtheme_uid):
    '''
        Display the content of the folder linked to the Galery object
    '''
    subtheme = SubTheme.objects.get(pk = subtheme_uid)
    if request.method == "POST" and request.user in subtheme.theme.authorized_user.all():
        form = NewItemForm(request.POST)
        if form.is_valid():
            new_item = Item()
            new_item.name = form.cleaned_data['name']
            new_item.subtheme = subtheme
            new_item.is_active = True
            new_item.created_date = timezone.now()
            theme = subtheme.theme
            new_item.save()
            # log it
            log = EventLog()
            log.author = request.user
            log.entity_type = 'item'
            log.value = str(new_item.name)[0:40]
            log.entity_uid = Item.objects.all().order_by('created_date').last().uid
            log.action = 'Création'
            log.theme = theme
            log.save()
            return HttpResponseRedirect(
                '/roadmap/view/{}'.format(subtheme.theme.uid))
        else:
            return HttpResponseRedirect(
                '/nope')
    else:
        context = {
            'subtheme' : subtheme,
            'new_item_form' : NewItemForm(),
            'page_title' : 'Nouvel item',
        }
        template = loader.get_template('roadmap/add_item.html')
        return HttpResponse(template.render(context, request))

@login_required
#####################################################################
def AddItemComment(request, item_uid):
    '''
        Display the content of the folder linked to the Galery object
    '''
    item = Item.objects.get(pk = item_uid)
    subtheme = item.subtheme
    if request.method == "POST" and request.user in subtheme.theme.authorized_user.all():
        form = NewItemCommentForm(request.POST)
        if form.is_valid():
            new_item = ItemComment()
            new_item.name = form.cleaned_data['name']
            new_item.item = item
            new_item.author = User.objects.get(pk = request.user.id)
            new_item.timestamp = timezone.now()
            new_item.save()
            # log it
            log = EventLog()
            log.author = request.user
            log.entity_type = 'commentaire'
            log.entity_uid = ItemComment.objects.all().order_by('created_date').last().uid
            log.value = str(new_item.name)[0:40]
            log.action = 'Création'
            log.theme = subtheme.theme
            log.save()
            return HttpResponseRedirect(
                '/roadmap/view/{}'.format(item.subtheme.theme.uid))
        else:
            return HttpResponseRedirect(
                '/nope')
    else:
        context = {
            'item': item,
            'new_item_comment_form' : NewItemCommentForm(),
            'page_title' : 'Nouveau commentaire',
        }
        template = loader.get_template('roadmap/add_item_comment.html')
        return HttpResponse(template.render(context, request))

@login_required
#####################################################################
def AddSubTheme(request, theme_uid):
    '''
        Display the content of the folder linked to the Galery object
    '''
    theme = Theme.objects.get(pk = theme_uid)
    if request.method == "POST"  and request.user in theme.authorized_user.all():
        form = NewSubThemeForm(request.POST)
        if form.is_valid():
            new_subtheme = SubTheme()
            new_subtheme.name = form.cleaned_data['name']
            new_subtheme.order = 0
            new_subtheme.author = User.objects.get(pk = request.user.id)
            new_subtheme.theme = theme
            new_subtheme.timestamp = timezone.now()
            new_subtheme.theme = theme
            new_subtheme.save()
            # Give it the right order
            for subtheme in SubTheme.objects.filter(theme = theme):
                subtheme.order += 1
                subtheme.save()
            # log it
            log = EventLog()
            log.author = request.user
            log.entity_type = 'sous-thème'
            log.entity_uid = SubTheme.objects.all().order_by('created_date').last().uid
            log.action = 'Création'
            log.theme = theme
            log.value = str(new_subtheme.name)[0:40]
            log.save()
            return HttpResponseRedirect(
                '/roadmap/view/{}'.format(theme.uid))
        else:
            return HttpResponseRedirect(
                '/nope')
    else:
        return HttpResponseRedirect('/roadmap/view/{}'.format(theme.uid))

@login_required
#####################################################################
def ItemStatusSwitch(request, item_uid, item_action):
    '''
        An todo item is_active status can be switched with this view.
    '''
    item = Item.objects.get(pk=item_uid)
    subtheme = item.subtheme
    theme = subtheme.theme
    if item_action == 'active_switch' and request.user in theme.authorized_user.all():
        if item.is_active == True:
            item.is_active = False
            item.is_important = False
            item.completed_date = timezone.now()
            item.save()
            # log it
            log = EventLog()
            log.author = request.user
            log.entity_type = 'item'
            log.entity_uid = Item.objects.all().order_by('created_date').last().uid
            log.action = 'Complétion'
            log.theme = theme
            log.save()
        else:
            item.is_active = True
            item.completed_date = None
            item.save()
            # log it
            log = EventLog()
            log.author = request.user
            log.entity_type = 'item'
            log.entity_uid = Item.objects.all().order_by('created_date').last().uid
            log.action = 'Réactivation'
            log.theme = theme
            log.save()
    elif item_action == 'importance_switch' and request.user in theme.authorized_user.all():
        if item.is_important == True:
            item.is_important = False
            item.save()
            # log it
            log = EventLog()
            log.author = request.user
            log.entity_type = 'item'
            log.entity_uid = Item.objects.all().order_by('created_date').last().uid
            log.action = 'Priorité abaissée'
            log.theme = theme
            log.save()
        else:
            item.is_important = True
            item.save()
            # log it
            log = EventLog()
            log.author = request.user
            log.entity_type = 'item'
            log.entity_uid = Item.objects.all().order_by('created_date').last().uid
            log.action = 'Priorité élevée'
            log.theme = theme
            log.save()
    else:
        return HttpResponseRedirect(
            '/nope')

    return HttpResponseRedirect('/roadmap/view/{}'.format(theme.uid))

@login_required
#####################################################################
def SubThemeOrderChange(request, subtheme_uid, subtheme_action):
    '''
        Users are allowed to change the order of subthemes.
        This view handles the ordrer change and the order change 
        of the other subthemes to adapt to the new order value of 
        the changed subtheme.
    '''
    subtheme = SubTheme.objects.get(pk = subtheme_uid)
    if subtheme_action == 'to_up':
        order_modificator = -1
    elif subtheme_action == 'to_down':
        order_modificator = 1
    else:
        return HttpResponseRedirect('/nope')
    if request.user in subtheme.theme.authorized_user.all():
        # check if order is already at minimum value
        if subtheme.order <= 1:
            return HttpResponseRedirect(
                '/roadmap/view/{}'.format(subtheme.theme.uid))
        else:
            pass
        # Do the modification
        try:
            subtheme.order += order_modificator
            subtheme_to_swap = SubTheme.objects.get(
                theme = subtheme.theme, order = subtheme.order)
            subtheme.save()
        except ObjectDoesNotExist:
            return HttpResponseRedirect(
                '/roadmap/view/{}'.format(subtheme.theme.uid))    
        # rearrange the item 
        subtheme_to_swap.order += -order_modificator
        subtheme_to_swap.save()
        return HttpResponseRedirect(
                '/roadmap/view/{}'.format(subtheme.theme.uid))
    else:
        return HttpResponseRedirect('/nope')