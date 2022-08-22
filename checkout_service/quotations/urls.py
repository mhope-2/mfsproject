from django.contrib import admin
from django.urls import path, include
from .views import QuotationsViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('quotations', QuotationsViewSet, basename='Quotations')


urlpatterns = [
    path('', include(router.urls)),

    path('quotations', QuotationsViewSet.as_view({
        'get': 'list',
    }), name='quotations'),

    path('quotation/create', QuotationsViewSet.as_view({
        'post': 'create',
    }), name='create-quotation'),

    path('quotation/<str:pk>/update', QuotationsViewSet.as_view({
        'put': 'update',
    }), name='update-quotation'),

    path('quotations/<str:pk>', QuotationsViewSet.as_view({
        'get': 'retrieve',
    }), name='retrieve-quotation'),

    path('quotations/<str:pk>/delete', QuotationsViewSet.as_view({
        'delete': 'destroy'
    }), name='delete-quotation')
]