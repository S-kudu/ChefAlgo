import requests
from bs4 import BeautifulSoup
from dashboard.models import Recipe

def scrape_recipes():
    url = "https://www.nefisyemektarifleri.com/kategori/tarifler/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    recipes = soup.find_all("div", class_="tarif-card")

    for recipe in recipes:
        title = recipe.find("h2").text.strip()
        image = recipe.find("img")["data-src"]

        Recipe.objects.get_or_create(
            title=title,
            defaults={
                "description": "Henüz açıklama yok",
                "image_url": image,
                "prep_time": 30,
                "difficulty": "Orta",
                "calories": 250,
            }
        )
