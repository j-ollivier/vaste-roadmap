from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from precise_bbcode.fields import BBCodeTextField



#####################################################################
class Theme(models.Model):
    '''
        Todo items are listed under a theme. Aka category, directory,
        etc.
    '''
    # Attributes
    uid = models.AutoField(
        primary_key = True, db_index = True)
    name = models.CharField(
        max_length = 100)
    authorized_user = models.ManyToManyField(
        User, 
        related_name= 'theme_authorized_user')
    author = models.ForeignKey(
        User, 
        models.SET_NULL,
        null = True,
        related_name = 'theme_author')
    timestamp =  models.DateTimeField(
        default = timezone.now)
    # Methods
    def __str__(self):
        return str(self.name)

#####################################################################
class SubTheme(models.Model):
    '''
        Todo subthemes are listed under a theme. Aka category, 
        directory, etc.
    '''
    # Attributes
    uid = models.AutoField(
        primary_key = True, db_index = True)
    name = models.CharField(
        max_length = 100)
    order = models.PositiveIntegerField(
        default = 0)
    author = models.ForeignKey(
        User, 
        models.SET_NULL,
        null = True,
        related_name = 'subtheme_author')
    theme = models.ForeignKey(
        Theme,
        on_delete = models.CASCADE,
        related_name= 'subtheme_theme')
    timestamp =  models.DateTimeField(
        default = timezone.now)
    # Methods
    def __str__(self):
        return str(self.name)
    def ItemCount(self):
        item_count = Item.objects.filter(
            subtheme = self).count()
        return item_count
    def ItemCountActive(self):
        item_count_active = Item.objects.filter(
            subtheme = self, is_active = True).count()
        return item_count_active

#####################################################################
class Item(models.Model):
    '''
        A todo item, possibily having a related Item to nest in.
    '''
    class Meta:
            ordering = ['-created_date']
    # Attributes
    uid = models.AutoField(
        primary_key = True, db_index = True)
    name = BBCodeTextField(
        )
    subtheme = models.ForeignKey(
        SubTheme,
        on_delete = models.CASCADE,
        related_name= 'item_subtheme')
    is_active = models.BooleanField(
        default = True)
    is_important = models.BooleanField(
        default = False)
    created_date =  models.DateTimeField(
        null = True)
    completed_date =  models.DateTimeField(
        default = timezone.now)
    # Methods
    def __str__(self):
        return str(self.name)

#####################################################################
class ItemComment(models.Model):
    '''
        Comments and logging utilities for each item
    '''
    class Meta:
            ordering = ['timestamp']
    # Attributes
    uid = models.AutoField(
        primary_key = True, db_index = True)
    name = models.CharField(
        max_length = 200
        )
    item = models.ForeignKey(
        Item,
        on_delete = models.CASCADE,
        related_name= 'item_comment_item')
    author = models.ForeignKey(
        User, 
        on_delete = models.CASCADE,
        related_name = 'item_comment_author')
    timestamp =  models.DateTimeField(
        default = timezone.now)
    # Methods
    def __str__(self):
        return str(self.name)