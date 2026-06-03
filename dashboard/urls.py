from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("panel/", views.dashboard, name="dashboard"),
    path("panel/ai/", views.ai_page, name="ai_page"),

    path("favorilerim/", views.favorites_page, name="favorites_page"),
    path("favori/<int:recipe_id>/", views.toggle_favorite, name="toggle_favorite"),

    path("hakkimizda/", views.about_page, name="about_page"),
    path("dokumantasyon/", views.documentation_page, name="documentation_page"),
    path("api-referansi/", views.api_reference_page, name="api_reference_page"),
    path("guvenlik/", views.security_page, name="security_page"),

    path("tarif/<slug:slug>/", views.recipe_detail, name="recipe_detail"),
]