from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, OrderViewSet, PostViewSet, ProductViewSet,
                    SaleViewSet, UserViewSet)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('products', ProductViewSet, basename='products')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('sales', SaleViewSet, basename='sales')
router_v1.register('orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.authtoken')),
]
