from django.contrib import admin
from .models import Category, Recipe


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "time", "difficulty", "score")
    list_filter = ("category", "difficulty")
    search_fields = ("title", "description", "ingredients")
    prepopulated_fields = {"slug": ("title",)}