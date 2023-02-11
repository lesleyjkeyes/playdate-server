"""playdate URL Configuration"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from playdateapi.views import UserView, MessageView, PetView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserView, 'user')
router.register(r'pets', PetView, 'user')
router.register(r'messages', MessageView, 'message')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
