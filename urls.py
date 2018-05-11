"""ogre URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from .views import *
from .models import *

urlpatterns = [
    path('', Home, name= 'Home'), 
    path('view/<int:theme_uid>', ThemeView),
    path('itemstatusswitch/<int:item_uid>/<str:item_action>', ItemStatusSwitch),
    path('additem/<int:subtheme_uid>', AddItem),
    path('additemcomment/<int:item_uid>', AddItemComment),
    path('addsubtheme/<int:theme_uid>', AddSubTheme),
]
