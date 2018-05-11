from django.contrib import admin
from .models import *

#####################################################################
class AdminTheme(admin.ModelAdmin):
    list_display= ['uid', 'name', 'author', 'timestamp']
    ordering= ['timestamp']
admin.site.register(Theme, AdminTheme)

#####################################################################
class AdminSubTheme(admin.ModelAdmin):
    list_display= ['uid', 'name', 'author', 'timestamp']
    ordering= ['timestamp']
admin.site.register(SubTheme, AdminSubTheme)

#####################################################################
class AdminItem(admin.ModelAdmin):
    list_display= ['uid', 'name', 'subtheme', 'created_date', 'completed_date', 'is_active', 'is_important']
    ordering= ['subtheme']
admin.site.register(Item, AdminItem)

#####################################################################
class AdminItemComment(admin.ModelAdmin):
    list_display= ['uid', 'name', 'item', 'author', 'timestamp']
    ordering= ['-timestamp']
admin.site.register(ItemComment, AdminItemComment)