from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from cart.models import Cart
from favorite.models import Favorite
from orders.models import Order
from posts.models import Category, Post, Product, Sale, User

from .permissions import IsAdminOrReadOnly, IsOwner
from .serializers import (CartSerializer, CategorySerializer,
                          FavoriteSerializer, OrderItemSerializer,
                          OrderSerializer, PostSerializer, ProductSerializer,
                          SaleSerializer, UserSerializer)


class ProductViewSet(viewsets.ModelViewSet):
    """
    Вывод списка товаров.
    Просмотр объекта по ID.
    Возможность добавления/удаления товара в корзину/избранное
    для авторизованных пользователей.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly,)

    @action(detail=True, permission_classes=(permissions.IsAuthenticated,))
    def cart(self, request, pk=None):
        context = {'request': request}
        user = request.user
        product = get_object_or_404(Product, id=pk)
        data = {
            'user': user.id,
            'product': product.id,
        }
        serializer = CartSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @cart.mapping.delete
    def cart_remove(self, request, pk=None):
        user = request.user
        product = get_object_or_404(Product, id=pk)
        get_object_or_404(Cart, user=user, product=product).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, permission_classes=(permissions.IsAuthenticated,))
    def favorite(self, request, pk=None):
        context = {'request': request}
        user = request.user
        product = get_object_or_404(Product, id=pk)
        data = {
            'user': user.id,
            'product': product.id,
        }
        serializer = FavoriteSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def favorite_remove(self, request, pk=None):
        user = request.user
        product = get_object_or_404(Product, id=pk)
        get_object_or_404(Favorite, user=user, product=product).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вывод списка категорий.
    Просмотр объекта по ID.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вывод списка постов.
    Просмотр объекта по ID.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class SaleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вывод списка выкладок.
    Просмотр объекта по ID.
    """

    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


class UserViewSet(DjoserUserViewSet):
    """
    Вьюсет для работы с пользователями.
    Список всех пользователей доступен только админу.
    Возможен просмотр только своего профиля.
    Регистрация, Логин/Логаут, смена пароля.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Вьюсет для работы с заказами.
    Выводит список заказов авторизованного пользователя.
    Возможен просмотр только своих заказов.
    Возможность создания заказа при условии непустой корзины.
    """

    serializer_class = OrderSerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.all()
        if self.action == "list" and not user.is_staff:
            queryset = queryset.filter(user=user)
        return queryset

    def create(self, request):
        context = {'request': request}
        user = request.user
        data = request.data
        serializer = OrderSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cart = Cart.objects.filter(user=user)
        for item in cart:
            order_data = {
                'product': item.product.id,
                'order': serializer.data['id'],
            }
            item_serializer = OrderItemSerializer(data=order_data)
            item_serializer.is_valid(raise_exception=True)
            item_serializer.save()
            data = {
                'owner': user,
                'is_available': False,
            }
            product = get_object_or_404(Product, id=item.product.id)
            get_object_or_404(Cart, user=user, product=product).delete()
            product.owner = data['owner']
            product.is_available = data['is_available']
            product.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
