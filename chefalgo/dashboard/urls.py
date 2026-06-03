from django.urls import path
from . import views

app_name="dashboard"
urlpatterns = [
    path("", views.home, name="home"),          # ana sayfa
    path("panel/", views.dashboard, name="panel"),  # dashboard paneli

    path('recipe/<int:id>/', views.recipe_detail, name='recipe_detail'),
]
