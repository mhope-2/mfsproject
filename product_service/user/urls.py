from django.contrib import admin
from django.urls import path, include
from .views import UserViewSet
                    

from rest_framework import routers


router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='User')

urlpatterns = [
    path('', include(router.urls)),
    path('users', UserViewSet.as_view({
        'get': 'list',
    })),
    path('users/create', UserViewSet.as_view({
        'post': 'create',
    })),
    path('users/<str:pk>', UserViewSet.as_view({
        'put': 'update'
    })),
    path('user/<str:pk>/retrieve', UserViewSet.as_view({
        'get': 'retrieve'
    })),
    path('user/<str:pk>/delete', UserViewSet.as_view({
        'delete': 'destroy'
    })),
    path('user/fetch', UserViewSet.as_view({
        'post': 'fetch',
    })),

    path('user/<str:pk>/delete', UserViewSet.as_view({
          'delete': 'destroy',
    })),

]