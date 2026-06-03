import requests
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from dashboard.models import Category, Recipe


DEFAULT_IMAGE = "https://images.unsplash.com/photo-1495521821757-a1efb6729352?auto=format&fit=crop&w=900&q=80"

CATEGORY_CONFIG = {
    "Çorbalar": {
        "queries": ["soup", "lentil soup", "tomato soup", "chicken soup", "vegetable soup", "mushroom soup"],
        "fallback_image": "https://images.unsplash.com/photo-1547592166-23ac45744acd?auto=format&fit=crop&w=900&q=80",
    },
    "Ana Yemekler": {
        "queries": ["chicken", "beef", "pasta", "rice", "vegetarian", "seafood", "lamb"],
        "fallback_image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=900&q=80",
    },
    "Tatlılar": {
        "queries": ["cake", "dessert", "chocolate", "pudding", "pie", "brownie", "cheesecake"],
        "fallback_image": "https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=900&q=80",
    },
    "İçecekler": {
        "queries": ["coffee", "lemonade", "smoothie", "milkshake", "tea", "juice"],
        "fallback_image": "https://images.unsplash.com/photo-1544145945-f90425340c7e?auto=format&fit=crop&w=900&q=80",
    },
    "Tuzlu Yiyecekler": {
        "queries": ["bread", "sandwich", "snack", "biscuit", "starter", "breakfast", "pastry"],
        "fallback_image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=900&q=80",
    },
}


def get_meals_by_search(query):
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={query}"
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
        return data.get("meals") or []
    except Exception:
        return []


def meal_to_recipe_data(meal, category_name, fallback_image):
    title = meal.get("strMeal") or "İsimsiz Tarif"
    image = meal.get("strMealThumb") or fallback_image or DEFAULT_IMAGE

    ingredients = []

    for i in range(1, 21):
        ingredient = meal.get(f"strIngredient{i}")
        measure = meal.get(f"strMeasure{i}")

        if ingredient and ingredient.strip():
            full_text = f"{measure or ''} {ingredient}".strip()
            ingredients.append(full_text)

    instructions = meal.get("strInstructions") or ""

    steps = [
        step.strip()
        for step in instructions.replace("\r", "").split("\n")
        if step.strip()
    ]

    if not steps and instructions:
        steps = [instructions]

    if not ingredients:
        ingredients = ["Malzeme bilgisi bulunamadı"]

    if not steps:
        steps = ["Hazırlanış bilgisi bulunamadı"]

    return {
        "title": title,
        "slug": slugify(title.replace("ı", "i")),
        "category": category_name,
        "description": f"{title} için internetten alınan tarif bilgisi.",
        "image": image,
        "time": "30 dakika",
        "prep_time": "10 dakika",
        "cook_time": "20 dakika",
        "calories": "Belirtilmedi",
        "servings": "4 kişilik",
        "difficulty": "Orta",
        "score": 90,
        "ingredients": "\n".join(ingredients),
        "steps": "\n".join(steps),
        "tips": "Tarife başlamadan önce tüm malzemeleri hazırlayın.",
        "serving_suggestion": "Taze ve sıcak şekilde servis edebilirsiniz.",
    }


class Command(BaseCommand):
    help = "İnternetten tarif çekip her kategoriye mümkün olduğunca çok tarif ekler."

    def handle(self, *args, **options):
        target_count = 40
        total_saved = 0

        for category_name, config in CATEGORY_CONFIG.items():
            category, _ = Category.objects.get_or_create(
                name=category_name,
                defaults={"icon": "bi-basket"}
            )

            fallback_image = config["fallback_image"]
            collected = {}

            self.stdout.write(self.style.WARNING(f"{category_name} için tarifler çekiliyor..."))

            for query in config["queries"]:
                meals = get_meals_by_search(query)

                for meal in meals:
                    title = meal.get("strMeal")

                    if title:
                        collected[title] = meal

                    if len(collected) >= target_count:
                        break

                if len(collected) >= target_count:
                    break

            saved_for_category = 0

            for meal in collected.values():
                data = meal_to_recipe_data(meal, category_name, fallback_image)

                Recipe.objects.update_or_create(
                    slug=data["slug"],
                    defaults={
                        "category": category,
                        "title": data["title"],
                        "description": data["description"],
                        "image": data["image"],
                        "time": data["time"],
                        "prep_time": data["prep_time"],
                        "cook_time": data["cook_time"],
                        "calories": data["calories"],
                        "servings": data["servings"],
                        "difficulty": data["difficulty"],
                        "score": data["score"],
                        "ingredients": data["ingredients"],
                        "steps": data["steps"],
                        "tips": data["tips"],
                        "serving_suggestion": data["serving_suggestion"],
                    }
                )

                saved_for_category += 1
                total_saved += 1

                if saved_for_category >= target_count:
                    break

            self.stdout.write(
                self.style.SUCCESS(
                    f"{category_name}: {saved_for_category} tarif eklendi/güncellendi."
                )
            )

        self.stdout.write(self.style.SUCCESS(f"Toplam {total_saved} tarif işlendi."))