from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('products', ProductsViewSet, basename='Products')


urlpatterns = [
    path('', include(router.urls)),

    # products
    path('products', ProductsViewSet.as_view({
        'get': 'list',
    })),
    path('products/create', ProductsViewSet.as_view({
        'post': 'create',
    })),
    path('products/<str:pk>/update', ProductsViewSet.as_view({
        'put': 'update',
    })),
    path('products/<str:pk>', ProductsViewSet.as_view({
        'get': 'retrieve',
    })),
    path('products/<str:pk>/delete', ProductsViewSet.as_view({
        'delete': 'destroy'
    })),

    path('products/product/search', ProductsViewSet.as_view({
            'post': 'product_search'
        })),
    
]
