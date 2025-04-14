Отлично! Вот **оформленная документация в Markdown**, описывающая твои Django-модели и методы. Подойдёт для `README.md`, wiki-проекта или автогенерации документации.

---

# 📦 Django модели каталога товаров

## Содержание

- [Category](#category)
- [Product](#product)
- [ProductManager](#productmanager)
- [ProductProxy](#productproxy)
- [Вспомогательные функции](#вспомогательные-функции)

---

## `Category`

Модель для описания иерархических категорий товаров.

| Поле         | Тип                            | Описание                      |
|--------------|--------------------------------|-------------------------------|
| `name`       | `CharField(max_length=250)`    | Название категории            |
| `parent`     | `ForeignKey('self')`           | Родительская категория        |
| `slug`       | `SlugField(max_length=250)`    | URL-идентификатор категории   |
| `created_at` | `DateTimeField(auto_now_add)`  | Дата создания                 |

### Особенности:

- Поддержка вложенных категорий.
- Уникальность пары `(slug, parent)`.
- Генерация `slug`, если он не указан.
- Метод `__str__()` возвращает путь вида: `Электроника > Смартфоны`.

---

## `Product`

Модель описания товара.

| Поле         | Тип                                              | Описание                      |
|--------------|--------------------------------------------------|-------------------------------|
| `title`      | `CharField(max_length=250)`                      | Название товара               |
| `category`   | `ForeignKey(Category)`                           | Категория                     |
| `brand`      | `CharField(max_length=250)`                      | Производитель (бренд)         |
| `description`| `TextField(blank=True)`                          | Описание                      |
| `slug`       | `SlugField(max_length=250)`                      | URL товара                    |
| `price`      | `DecimalField(max_digits=10, decimal_places=2)` | Цена                          |
| `image`      | `ImageField(upload_to='products/…')`             | Фото товара                   |
| `available`  | `BooleanField(default=True)`                     | Наличие на складе             |
| `created_at` | `DateTimeField(auto_now_add)`                    | Дата добавления               |
| `updated_at` | `DateTimeField(auto_now)`                        | Дата последнего изменения     |

---

## `ProductManager`

Менеджер для фильтрации доступных (в наличии) товаров.

```python
class ProductManager(models.Model):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(available=True)
```

---

## `ProductProxy`

Прокси-модель, использующая `ProductManager` для получения только доступных товаров.

```python
class ProductProxy(Product):
    objects = ProductManager()

    class Meta:
        proxy = True
```

---

## Вспомогательные функции

### `random_slug() -> str`

Генерирует случайный короткий slug (3 символа) из латинских букв и цифр.  
Используется для формирования уникального `slug` категории, если он не задан вручную.

```python
def random_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))
```

---
