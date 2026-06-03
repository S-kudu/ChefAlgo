from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Category, Recipe, Favorite


def normalize_text(text):
    return (text or "").lower() \
        .replace("ı", "i") \
        .replace("İ", "i") \
        .replace("ğ", "g") \
        .replace("ü", "u") \
        .replace("ş", "s") \
        .replace("ö", "o") \
        .replace("ç", "c") \
        .strip()


def split_words(text):
    return [
        normalize_text(word)
        for word in text.replace(",", " ").split()
        if len(normalize_text(word)) > 1
    ]


def home(request):
    return render(request, "home.html")


def dashboard(request):
    selected_category = request.GET.get("category", "").strip()
    search_query = request.GET.get("q", "").strip()
    ingredient_query = request.GET.get("ingredients", "").strip()

    categories = Category.objects.all()
    recipes_queryset = Recipe.objects.select_related("category").all()
    recipes = recipes_queryset

    selected_category_name = ""
    page_title = "Tüm Tarifler"
    ingredient_mode = False
    ingredient_words = []

    # Kategori filtresi
    if selected_category:
        matched_category = None

        for category in categories:
            if normalize_text(category.name) == normalize_text(selected_category):
                matched_category = category
                break

        if matched_category:
            recipes = recipes.filter(category=matched_category)
            selected_category_name = matched_category.name
            page_title = f"{matched_category.name} Tarifleri"

    # Normal arama
    if search_query:
        q = normalize_text(search_query)
        matched = []

        for recipe in recipes:
            area = " ".join([
                recipe.title,
                recipe.description,
                recipe.ingredients,
                recipe.category.name,
            ])

            if q in normalize_text(area):
                matched.append(recipe)

        recipes = matched
        selected_category_name = ""
        page_title = f"“{search_query}” için sonuçlar"

    # ChefAlgo AI - malzemeye göre tarif önerme
    if ingredient_query:
        ingredient_mode = True
        ingredient_words = split_words(ingredient_query)
        scored_results = []

        if ingredient_words:
            for recipe in recipes_queryset:
                recipe_area = normalize_text(" ".join([
                    recipe.title,
                    recipe.description,
                    recipe.ingredients,
                    recipe.category.name,
                ]))

                matched_count = 0
                missing_words = []

                for word in ingredient_words:
                    if word in recipe_area:
                        matched_count += 1
                    else:
                        missing_words.append(word)

                if matched_count > 0:
                    score_percent = int((matched_count / len(ingredient_words)) * 100)

                    recipe.match_count = matched_count
                    recipe.match_percent = score_percent
                    recipe.missing_count = len(missing_words)
                    recipe.missing_words = missing_words

                    scored_results.append((recipe, score_percent, matched_count))

            scored_results.sort(key=lambda item: (item[1], item[2]), reverse=True)
            recipes = [item[0] for item in scored_results]

        else:
            recipes = []

        selected_category_name = ""
        page_title = "Elindeki malzemelere göre öneriler"

    category_stats = [
        (category.name, Recipe.objects.filter(category=category).count())
        for category in categories
    ]

    total_ingredients = sum(
        len(recipe.ingredient_list())
        for recipe in Recipe.objects.all()
    )

    favorite_recipe_ids = []

    if request.user.is_authenticated:
        favorite_recipe_ids = list(
            Favorite.objects.filter(
                user=request.user
            ).values_list("recipe_id", flat=True)
        )

    context = {
        "total_recipes": Recipe.objects.count(),
        "total_ingredients": total_ingredients,
        "algo_score": 98.4,
        "categories": categories,
        "selected_category": selected_category_name,
        "category_stats": category_stats,
        "recent_recipes": recipes,
        "search_query": search_query,
        "ingredient_query": ingredient_query,
        "ingredient_words": ingredient_words,
        "ingredient_mode": ingredient_mode,
        "page_title": page_title,
        "favorite_recipe_ids": favorite_recipe_ids,
    }

    return render(request, "dashboard.html", context)


def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)

    similar_recipes = Recipe.objects.filter(
        category=recipe.category
    ).exclude(id=recipe.id)[:3]

    is_favorite = False

    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists()

    return render(request, "recipe_detail.html", {
        "recipe": recipe,
        "similar_recipes": similar_recipes,
        "categories": Category.objects.all(),
        "is_favorite": is_favorite,
    })


@login_required
def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        recipe=recipe
    )

    if not created:
        favorite.delete()

    next_url = request.GET.get("next")

    if next_url:
        return redirect(next_url)

    return redirect("dashboard")


@login_required
def favorites_page(request):
    favorite_recipes = Recipe.objects.filter(
        favorites__user=request.user
    ).select_related("category")

    context = {
        "favorite_recipes": favorite_recipes,
    }

    return render(request, "favorites.html", context)


def ai_page(request):
    ingredient_query = request.GET.get("ingredients", "").strip()

    recipes_queryset = Recipe.objects.select_related("category").all()

    ingredient_mode = False
    ingredient_words = []
    recipes = []

    perfect_matches = []
    good_matches = []
    low_matches = []

    if ingredient_query:
        ingredient_mode = True
        ingredient_words = split_words(ingredient_query)
        scored_results = []

        if ingredient_words:
            for recipe in recipes_queryset:
                recipe_ingredients_text = normalize_text(recipe.ingredients)
                recipe_general_text = normalize_text(" ".join([
                    recipe.title,
                    recipe.description,
                    recipe.category.name,
                ]))

                matched_words = []
                missing_words = []
                score = 0

                for word in ingredient_words:
                    if word in recipe_ingredients_text:
                        matched_words.append(word)
                        score += 3
                    elif word in recipe_general_text:
                        matched_words.append(word)
                        score += 1
                    else:
                        missing_words.append(word)

                if matched_words:
                    max_score = len(ingredient_words) * 3
                    score_percent = int((score / max_score) * 100)

                    recipe.match_count = len(matched_words)
                    recipe.match_percent = score_percent
                    recipe.missing_count = len(missing_words)
                    recipe.matched_words = matched_words
                    recipe.missing_words = missing_words

                    scored_results.append((recipe, score_percent, len(matched_words)))

            scored_results.sort(key=lambda item: (item[1], item[2]), reverse=True)
            recipes = [item[0] for item in scored_results]

            for recipe in recipes:
                if recipe.match_percent >= 90:
                    perfect_matches.append(recipe)
                elif recipe.match_percent >= 60:
                    good_matches.append(recipe)
                else:
                    low_matches.append(recipe)

    favorite_recipe_ids = []

    if request.user.is_authenticated:
        favorite_recipe_ids = list(
            Favorite.objects.filter(
                user=request.user
            ).values_list("recipe_id", flat=True)
        )

    context = {
        "ingredient_query": ingredient_query,
        "ingredient_words": ingredient_words,
        "ingredient_mode": ingredient_mode,
        "recipes": recipes,
        "perfect_matches": perfect_matches,
        "good_matches": good_matches,
        "low_matches": low_matches,
        "favorite_recipe_ids": favorite_recipe_ids,
    }

    return render(request, "ai_page.html", context)

def about_page(request):
    return render(request, "corporate/about.html")


def documentation_page(request):
    return render(request, "corporate/documentation.html")


def api_reference_page(request):
    return render(request, "corporate/api_reference.html")


def security_page(request):
    return render(request, "corporate/security.html")