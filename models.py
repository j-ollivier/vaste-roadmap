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
    created_date =  models.DateTimeField(
        default = timezone.now)
    # Methods
    def __str__(self):
        return str(self.name)
    def SubThemeActivity(self):
        # fetching all subthemes
        subthemes = SubTheme.objects.filter(theme = self)
        subtheme_activity = list(EventLog.objects.filter(
            entity_type = 'sous-thème', 
            entity_uid__in = [i.uid for i in subthemes]))
        return subtheme_activity


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
    author = models.ForeignKey(
        User, 
        models.SET_NULL,
        null = True,
        related_name = 'subtheme_author')
    theme = models.ForeignKey(
        Theme,
        on_delete = models.CASCADE,
        related_name= 'subtheme_theme')
    order = models.PositiveIntegerField(
       )
    created_date =  models.DateTimeField(
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
    def ItemActivity(self):
        # fetching all subthemes
        items = Item.objects.filter(subtheme = self)
        item_activity = EventLog.objects.filter(
            entity_type = 'item', 
            entity_uid__in = [i.uid for i in items])
        return item_activity

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
        default = timezone.now)
    completed_date =  models.DateTimeField(
        null = True)
    attributed_to = models.ForeignKey(
        User,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
        related_name = 'item_user')
    # Methods
    def __str__(self):
        return str(self.name)
    def ItemCommentActivity(self):
        # fetching all subthemes
        comments = ItemComment.objects.filter(item = self)
        item_comment_activity = EventLog.objects.filter(
            entity_type = 'item', 
            entity_uid__in = [i.uid for i in comments])
        return item_comment_activity

#####################################################################
class ItemComment(models.Model):
    '''
        Comments and logging utilities for each item
    '''
    class Meta:
            ordering = ['created_date']
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
    created_date =  models.DateTimeField(
        default = timezone.now)
    # Methods
    def __str__(self):
        return str(self.name)

#####################################################################
class EventLog(models.Model):
    '''
        To keep track of every event, a log entry is available each
        time an event happens in
    '''
    class Meta:
            ordering = ['-created_date']
    # Attributes
    uid = models.AutoField(
        primary_key = True, db_index = True)
    author = models.ForeignKey(
        User, 
        on_delete = models.CASCADE,
        related_name = 'log_author')
    theme = models.ForeignKey(
        Theme,
        on_delete = models.CASCADE,
        related_name = 'log_theme')
    entity_uid = models.PositiveIntegerField(
        )
    entity_type = models.CharField(
        max_length = 100)
    value = models.TextField(
        null = True)
    action = models.CharField(
        max_length = 200)
    created_date =  models.DateTimeField(
        default = timezone.now)
    # Methods
    def __str__(self):
        return str(self.uid)