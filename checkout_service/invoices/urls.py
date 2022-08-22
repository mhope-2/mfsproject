from django.urls import path, include
from .views import InvoicesViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('invoices', InvoicesViewSet, basename='Invoices')


urlpatterns = [
    path('', include(router.urls)),

    # invoices
    path('invoices', InvoicesViewSet.as_view({
        'get': 'list',
    })),

    path('invoices/create', InvoicesViewSet.as_view({
        'post': 'create',
    }), name='create-invoice'),

    path('invoices/<str:pk>/retrieve', InvoicesViewSet.as_view({
        'get': 'retrieve',
    }), name='retrieve-invoice'),

]
