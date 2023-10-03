from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from cart.models import Cart
from favorite.models import Favorite
from orders.models import Order, OrderItem
from posts.models import Category, Post, Product, Sale, User


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор модели товаров"""

    class Meta:
        model = Product
        exclude = ('owner', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели категорий"""

    products = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class UserSerializer(UserSerializer):
    """Сериализатор модели пользователя"""

    cart = serializers.StringRelatedField(many=True, read_only=True)
    products = serializers.StringRelatedField(many=True, read_only=True)
    favorite = serializers.StringRelatedField(many=True, read_only=True)
    orders = serializers.StringRelatedField(many=True, read_only=True)
    cart_price = serializers.SerializerMethodField()

    def get_cart_price(self, obj):
        print(obj)
        cart = Cart.objects.filter(user=obj)
        return sum(item.product.price for item in cart)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'favorite',
            'cart',
            'cart_price',
            'products',
            'orders',
        )


class UserCreateSerializer(UserCreateSerializer):
    """Сериализатор создания пользователя"""

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class SaleSerializer(serializers.ModelSerializer):
    """Сериализатор модели выкладки"""

    products = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор модели постов"""

    class Meta:
        model = Post
        exclude = ('pub_date',)


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор модели избранного"""

    class Meta:
        model = Favorite
        fields = '__all__'

    def validate(self, data):
        user = data['user']
        product = data['product']
        if user.favorite.filter(product=product).exists():
            raise serializers.ValidationError('Товар уже добавлен в избранное')
        return data


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор модели корзины"""

    class Meta:
        model = Cart
        fields = '__all__'

    def validate(self, data):
        user = data['user']
        product = data['product']
        if user.cart.filter(product=product).exists():
            raise serializers.ValidationError('Товар уже добавлен в корзину')
        if not product.is_available:
            raise serializers.ValidationError('Товар продан')
        return data


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор модели заказов"""

    products = serializers.StringRelatedField(many=True, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_price = serializers.SerializerMethodField()

    def get_order_price(self, obj):
        return sum(item.product.price for item in obj.products.all())

    class Meta:
        model = Order
        # fields = '__all__'
        exclude = ('paid',)

    def validate(self, data):
        user = data['user']
        if not user.cart.exists():
            raise serializers.ValidationError('Корзина пуста')
        return data


class OrderItemSerializer(serializers.ModelSerializer):
    """Сериализатор модели наполнения заказов"""

    class Meta:
        model = OrderItem
        fields = '__all__'
