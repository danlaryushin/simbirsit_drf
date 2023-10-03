from django.contrib.auth import get_user_model
from django.db import models

from posts.models import Product

User = get_user_model()


class Cart(models.Model):
    """
    Модель Корзины.

    Attributes:
        product(str):
            Товар. Связан с моделью Product через ForeignKey.
        user(int):
            Пользователь. Связан с моделью User через ForeignKey.
    """

    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart',
        unique=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
    )

    def __str__(self):
        return str(self.product.id)
