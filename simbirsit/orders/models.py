from django.db import models

from posts.models import Product, User


class Order(models.Model):
    """
    Модель Заказа.

    Attributes:
        user(int):
            Пользователь. Связан с моделью User через ForeignKey.
        first_name(str):
            Имя заказчика.
        last_name(str):
            Фамилия заказчика.
        email(str):
            Электронная почта заказчика.
        country(str):
            Страна для доставки.
        city(str):
            Город для доставки.
        address(str):
            Улица, дом для доставки.
        postal_code(str):
            Почтовый индекс.
        created(datetime):
            Дата создания заказа. Автозаполняемое поле.
        updated(datetime):
            Дата изменения заказа. Автозаполняемое поле.
        paid(bool):
            Статус оплаты заказа.
    """

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='orders', null=True
    )
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField()
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    postal_code = models.CharField(max_length=20, verbose_name='Индекс')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    paid = models.BooleanField(default=False, verbose_name='Оплачен')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.id)

    @property
    def order_price(self):
        return sum(item.product.price for item in self.products.all())


class OrderItem(models.Model):
    """
    Модель наполнения заказа.

    Attributes:
        order(int):
            Заказ. Связан с моделью Order через ForeignKey.
        product(str):
            Товар. Связан с моделью Product через ForeignKey.
    """

    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        Order, related_name='products', on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return str(self.product.id)
