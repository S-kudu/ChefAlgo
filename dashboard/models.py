from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, default="bi-basket")
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name.replace("ı", "i"))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ("Kolay", "Kolay"),
        ("Orta", "Orta"),
        ("Zor", "Zor"),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="recipes")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    image = models.URLField(blank=True)

    time = models.CharField(max_length=50, default="30 dakika")
    prep_time = models.CharField(max_length=50, default="10 dakika")
    cook_time = models.CharField(max_length=50, default="20 dakika")
    calories = models.CharField(max_length=50, default="Belirtilmedi")
    servings = models.CharField(max_length=50, default="4 kişilik")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default="Kolay")
    score = models.PositiveIntegerField(default=90)

    ingredients = models.TextField(help_text="Her malzemeyi yeni satıra yaz.")
    steps = models.TextField(help_text="Her adımı yeni satıra yaz.")
    tips = models.TextField(blank=True)
    serving_suggestion = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tarif"
        verbose_name_plural = "Tarifler"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title.replace("ı", "i"))
        super().save(*args, **kwargs)

    def ingredient_list(self):
        return [x.strip() for x in self.ingredients.splitlines() if x.strip()]

    def step_list(self):
        return [x.strip() for x in self.steps.splitlines() if x.strip()]

    def __str__(self):
        return self.title
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Favori"
        verbose_name_plural = "Favoriler"
        unique_together = ("user", "recipe")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.recipe.title}"