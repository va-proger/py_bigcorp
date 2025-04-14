"""
Модели для каталога товаров.

Содержит модели:
- Category: иерархическая структура категорий
- Product: описание товара
- ProductProxy: прокси-модель для доступных товаров
"""

from django.db import models
from django.utils.text import slugify
import random
import string
from django.urls import reverse

def random_slug():
    """
    Генерирует случайный slug из 3 символов, состоящих из букв и цифр.
    :return: строка
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))


class Category(models.Model):
    """
    Модель категории с возможностью иерархии (родительские/дочерние категории).
    """
    name = models.CharField("Категория", max_length=250, db_index=True)
    parent = models.ForeignKey(
        'self',
        verbose_name="Родительская категория",
        on_delete=models.CASCADE,
        related_name='children',
        blank=True,
        null=True,
    )
    slug = models.SlugField("URL", max_length=250, unique=True, null=False, editable=True, db_index=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        unique_together = ('slug', 'parent')
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """
        Возвращает полный путь категории с учётом иерархии.
        """
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

    def save(self, *args, **kwargs):
        """
        Переопределение метода сохранения: если slug не указан, он будет сгенерирован автоматически.
        """
        if not self.slug:
            self.slug = slugify(random_slug() + '-pickBetter' + self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Возвращает абсолютный URL для категории.
        """
        return reverse('shop:category-list', args=[str(self.slug)])


class Product(models.Model):
    """
    Модель продукта. Содержит информацию о названии, бренде, категории, цене и т. д.
    """
    title = models.CharField("Название", max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.CharField("Бренд", max_length=250)
    description = models.TextField("Описание", blank=True)
    slug = models.SlugField("URL", max_length=250)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2, default=99.99)
    image = models.ImageField("Изображение", upload_to='products/products/%Y/%m/%d', blank=True)
    available = models.BooleanField("Наличие", default=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        """
        Возвращает название продукта.
        """
        return self.title

    def get_absolute_url(self):
        """
        Возвращает абсолютный URL продукта.
        """
        return reverse('shop:product-detail', args=[str(self.slug)])


class ProductManager(models.Manager):
    """
    Менеджер для получения только доступных товаров.
    """
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):
    """
    Прокси-модель для фильтрации доступных товаров.
    """
    objects = ProductManager()

    class Meta:
        proxy = True
