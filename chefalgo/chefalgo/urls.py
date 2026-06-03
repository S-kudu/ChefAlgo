from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin paneli
    path("admin/", admin.site.urls),

    # Accounts uygulaması (kayıt, giriş, çıkış)
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),

    # Dashboard uygulaması (panel, istatistikler)
    path("", include(("dashboard.urls", "dashboard"), namespace="dashboard")),
]

# Geliştirme aşamasında statik ve medya dosyalarının okunması için şarttır:
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
