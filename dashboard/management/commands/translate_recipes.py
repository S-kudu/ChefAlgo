from django.core.management.base import BaseCommand
from deep_translator import GoogleTranslator

from dashboard.models import Recipe


def translate_text(translator, text):
    if not text:
        return ""

    try:
        return translator.translate(text)
    except Exception:
        return text


class Command(BaseCommand):
    help = "Veritabanındaki tarifleri Türkçeye çevirir."

    def handle(self, *args, **options):
        translator = GoogleTranslator(source="auto", target="tr")

        recipes = Recipe.objects.all()
        count = 0

        for recipe in recipes:
            old_title = recipe.title

            recipe.title = translate_text(translator, recipe.title)
            recipe.description = translate_text(translator, recipe.description)
            recipe.ingredients = translate_text(translator, recipe.ingredients)
            recipe.steps = translate_text(translator, recipe.steps)
            recipe.tips = translate_text(translator, recipe.tips)
            recipe.serving_suggestion = translate_text(translator, recipe.serving_suggestion)

            recipe.save()
            count += 1

            self.stdout.write(self.style.SUCCESS(f"Çevrildi: {old_title} -> {recipe.title}"))

        self.stdout.write(self.style.SUCCESS(f"Toplam {count} tarif çevrildi."))