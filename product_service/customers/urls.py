from django.contrib import admin
from django.urls import path, include
from .views import CustomerViewSet


from rest_framework import routers


router = routers.DefaultRouter()
router.register("customers", CustomerViewSet, basename="Customer")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "customers",
        CustomerViewSet.as_view(
            {
                "get": "list",
            }
        ),
        name="customers",
    ),
    path(
        "customers/create",
        CustomerViewSet.as_view(
            {
                "post": "create",
            }
        ),
        name="create-customer",
    ),
    path(
        "customer/<str:pk>/retrieve",
        CustomerViewSet.as_view(
            {
                "get": "retrieve",
            }
        ),
        name="retrieve-customer",
    ),
    path(
        "customers/<str:pk>/update",
        CustomerViewSet.as_view(
            {
                "put": "update",
            }
        ),
        name="update-customer",
    ),
    path(
        "customers/<str:pk>/delete",
        CustomerViewSet.as_view(
            {
                "delete": "destroy",
            }
        ),
        name="delete-customer",
    ),
]
