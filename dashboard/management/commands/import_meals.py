import requests
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from dashboard.models import Category, Recipe


CATEGORY_MAP = {
    "soup": "Çorbalar",
    "dessert": "Tatlılar",
    "beef": "Ana Yemekler",
    "chicken": "Ana Yemekler",
    "seafood": "Ana Yemekler",
    "pasta": "Ana Yemekler",
    "vegetarian": "Ana Yemekler",
    "starter": "Tuzlu Yiyecekler",
    "breakfast": "Tuzlu Yiyecekler",
    "side": "Tuzlu Yiyecekler",
}


class Command(BaseCommand):
    help = "TheMealDB API üzerinden tarifleri çekip veritabanına kaydeder."

    def add_arguments(self, parser):
        parser.add_argument(
            "query",
            type=str,
            help="Aranacak tarif kelimesi. Örn: soup, chicken, dessert"
        )

    def handle(self, *args, **options):
        query = options["query"].strip()

        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={query}"
        response = requests.get(url, timeout=20)
        data = response.json()

        meals = data.get("meals")

        if not meals:
            self.stdout.write(self.style.WARNING("Tarif bulunamadı. Başka kelime dene: soup, chicken, dessert"))
            return

        saved_count = 0

        for meal in meals:
            api_category = (meal.get("strCategory") or "").lower()
            site_category_name = CATEGORY_MAP.get(api_category, "Ana Yemekler")

            category, _ = Category.objects.get_or_create(
                name=site_category_name,
                defaults={"icon": "bi-basket"}
            )

            title = meal.get("strMeal") or "İsimsiz Tarif"
            slug = slugify(title.replace("ı", "i"))

            ingredients = []

            for i in range(1, 21):
                ingredient = meal.get(f"strIngredient{i}")
                measure = meal.get(f"strMeasure{i}")

                if ingredient and ingredient.strip():
                    text = f"{measure or ''} {ingredient}".strip()
                    ingredients.append(text)

            instructions = meal.get("strInstructions") or ""
            steps = [
                step.strip()
                for step in instructions.replace("\r", "").split("\n")
                if step.strip()
            ]

            if not steps and instructions:
                steps = [instructions]

            Recipe.objects.update_or_create(
                slug=slug,
                defaults={
                    "category": category,
                    "title": title,
                    "description": f"{title} için internetten alınan tarif bilgisi.",
                    "image": meal.get("strMealThumb") or "",
                    "time": "30 dakika",
                    "prep_time": "10 dakika",
                    "cook_time": "20 dakika",
                    "calories": "Belirtilmedi",
                    "servings": "4 kişilik",
                    "difficulty": "Orta",
                    "score": 90,
                    "ingredients": "\n".join(ingredients),
                    "steps": "\n".join(steps),
                    "tips": "Tarifi uygulamadan önce malzemeleri hazırlamanız pişirme sürecini kolaylaştırır.",
                    "serving_suggestion": "Sıcak ve taze şekilde servis edebilirsiniz.",
                }
            )

            saved_count += 1

        self.stdout.write(self.style.SUCCESS(f"{saved_count} tarif başarıyla veritabanına kaydedildi."))