from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    """
    Модель Категории.

    Attributes:
        title(str):
            Название категории.
        description(str):
            Описание категории.
        image(str):
            Фото категории.
    """

    id = models.AutoField(primary_key=True)
    title = models.TextField(verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(
        verbose_name='Фото категории', null=True, blank=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Product(models.Model):
    """
    Модель Товара.

    Attributes:
        number(int):
            Номер товара.
        image(str):
            Фото товара.
        video(str):
            Видео товара.
        title(str):
            Название товара.
        length(int):
            Длина товара.
        width(int):
            Ширина товара.
        price(int):
            Цена товара.
        is_available(bool):
            Статус товара: В наличии/продан.
        is_active(bool):
            Статус товара: Опубликован/скрыт.
        pub_date(datetime):
            Дата создания товара.
        category(int):
            Категория. Связана с моделью Category через ForeignKey.
        sale(int):
            Выкладка. Связана с моделью Sale через ForeignKey.
        owner(int):
            Покупатель. Связан с моделью User через ForeignKey.
            Автозаполняемое поле.
    """

    id = models.AutoField(primary_key=True)
    number = models.IntegerField(verbose_name='Номер')
    image = models.ImageField(
        null=True,
        upload_to='posts/',
        blank=True,
        verbose_name='Фото',
    )
    video = models.FileField(verbose_name='Видео', null=True, blank=True)
    title = models.TextField(verbose_name='Название')
    length = models.IntegerField(verbose_name='Длина')
    width = models.IntegerField(verbose_name='Ширина')
    price = models.PositiveIntegerField(verbose_name='Цена')
    is_available = models.BooleanField(default=True, verbose_name='В наличии')
    is_active = models.BooleanField(default=False, verbose_name='Опубликован')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        default=1,
        on_delete=models.SET_NULL,
        related_name='products',
        verbose_name='Категория',
    )
    sale = models.ForeignKey(
        'Sale',
        on_delete=models.SET_NULL,
        related_name='products',
        blank=True,
        null=True,
        verbose_name='Выкладка',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='products',
        verbose_name='Покупатель',
    )

    class Meta:
        ordering = ('-is_available', '-pub_date')
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return str(self.id)


class Sale(models.Model):
    """
    Модель Выкладки.

    Attributes:
        date(datetime):
            Дата создания выкладки.
    """

    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Выкладка'
        verbose_name_plural = 'Выкладки'

    def __str__(self):
        return f'Выкладка от {self.date.strftime("%Y-%m-%d")}'


class Post(models.Model):
    """
    Модель Поста.

    Attributes:
        image(str):
            Фото поста.
        pub_date(datetime):
            Дата создания поста.
        category(int):
            Категория. Связана с моделью Category через ForeignKey.
        sale(int):
            Выкладка. Связана с моделью Sale через ForeignKey.
    """

    id = models.AutoField(primary_key=True)
    image = models.ImageField(
        null=True,
        upload_to='posts/',
        blank=True,
        verbose_name='Фото',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Категория',
    )
    sale = models.ForeignKey(
        Sale,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Выкладка',
    )

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'
