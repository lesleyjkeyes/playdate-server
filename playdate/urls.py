"""playdate URL Configuration"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from playdateapi.views import UserView, MessageView, PetView, InterestView, TraitView, PetInterestView, PetTraitView, FollowView, check_user, register_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserView, 'user')
router.register(r'pets', PetView, 'user')
router.register(r'messages', MessageView, 'message')
router.register(r'interests', InterestView, 'interest')
router.register(r'traits', TraitView, 'trait')
router.register(r'petinterests', PetInterestView, 'petinterest')
router.register(r'pettraits', PetTraitView, 'pettrait')
router.register(r'follows', FollowView, 'follow')

urlpatterns = [
    path('register', register_user),
    path('checkuser', check_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
