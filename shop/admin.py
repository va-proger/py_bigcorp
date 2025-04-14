from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "slug")
    ordering = ("name",)

    def get_prepopulated_fields(self, request, obj=None):
        return {
            "slug":('name', ),
        }

    class Meta:
        model = Category
        fields = '__all__'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "brand",   "slug",  "price", "available", "created_at", "updated_at")
    ordering = ("title",)
    list_filter = ("available", "created_at", "updated_at")

    def get_prepopulated_fields(self, request, obj=None):
        return {
            "slug":('title', ),
        }

    class Meta:
        model = Product
        fields = '__all__'