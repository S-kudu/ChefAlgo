from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Recipe

def home(request):
    """
    Ana sayfa (Landing Page).
    Giriş yapmamış kullanıcılara projenin vizyonunu gösterir.
    """
    if request.user.is_authenticated:
        # return redirect('dashboard:panel')  # İstersen giriş yapanı direkt panele yönlendirebilirsin
        pass
    return render(request, 'home.html')


@login_required(login_url='accounts:login')
def dashboard(request):
    """
    Gelişmiş Kontrol Paneli (Dashboard).
    Hem istatistiksel veriler hem de Recipe modelinden gelen tarifler burada gösterilir.
    """

    # 1. Kategori Modülleri (örnek statik veri)
    categories = [
        {'name': 'Çorbalar', 'icon': 'bi-cup-hot', 'count': 15, 'color': 'primary'},
        {'name': 'Ana Yemekler', 'icon': 'bi-egg-fried', 'count': 45, 'color': 'success'},
        {'name': 'Tatlılar', 'icon': 'bi-cake2', 'count': 20, 'color': 'danger'},
        {'name': 'Soğuk İçecekler', 'icon': 'bi-snow', 'count': 35, 'color': 'info'},
        {'name': 'Sıcak İçecekler', 'icon': 'bi-moisture', 'count': 30, 'color': 'warning'},
    ]

    # 2. İstatistiksel Veriler
    stats = {
        'total_recipes': Recipe.objects.count(),   # artık gerçek veritabanı sayısı
        'total_ingredients': 82,
        'algo_score': 98.4,
    }

    # 3. Son Aktiviteler (örnek statik veri)
    recent_recipes = [
        {'title': 'Mantar Soslu Tavuk', 'time': '5 dakika önce', 'status': 'Optimize Edildi'},
        {'title': 'Sebzeli Ratatouille', 'time': '12 dakika önce', 'status': 'Analiz Edildi'},
        {'title': 'Kremalı Balkabağı Çorbası', 'time': '1 saat önce', 'status': 'Sıfır Atık'},
    ]

    # 4. Grafik Verileri
    chart_data = {
        'labels': [cat['name'] for cat in categories],
        'counts': [cat['count'] for cat in categories],
    }

    # 5. Scraper ile gelen tarifler
    recipes = Recipe.objects.all()

    context = {
        'categories': categories,
        'stats': stats,
        'recent_recipes': recent_recipes,
        'chart_data': chart_data,
        'recipes': recipes,
        'title': 'Mutfak Kontrol Merkezi'
    }

    return render(request, 'dashboard/dashboard.html', context)


def recipe_detail(request, id):
    """
    Tekil tarif detay sayfası.
    """
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'dashboard/detail.html', {'recipe': recipe})
