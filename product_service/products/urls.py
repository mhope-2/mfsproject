from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register("products", ProductsViewSet, basename="Products")


urlpatterns = [
    path("", include(router.urls)),
    # products
    path(
        "products",
        ProductsViewSet.as_view(
            {
                "get": "list",
            }
        ),
        name="products",
    ),
    path(
        "products/create",
        ProductsViewSet.as_view(
            {
                "post": "create",
            }
        ),
        name="create-product",
    ),
    path(
        "products/<str:pk>/update",
        ProductsViewSet.as_view(
            {
                "put": "update",
            }
        ),
        name="update-product",
    ),
    path(
        "product/<str:pk>/retrieve",
        ProductsViewSet.as_view(
            {
                "get": "retrieve",
            }
        ),
        name="retrieve-product",
    ),
    path(
        "products/<str:pk>/delete",
        ProductsViewSet.as_view({"delete": "destroy"}),
        name="delete-product",
    ),
    # path('products/product/search', ProductsViewSet.as_view({
    #     'post': 'product_search'
    # })),
]
