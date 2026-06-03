from django.core.management.base import BaseCommand
from django.utils.text import slugify

from dashboard.models import Category, Recipe


RECIPES = [
    {
        "category": "Tatlılar",
        "title": "Sütlaç",
        "description": "Süt, pirinç ve şekerle hazırlanan klasik hafif tatlı.",
        "image": "https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?auto=format&fit=crop&w=900&q=80",
        "time": "45 dakika",
        "prep_time": "10 dakika",
        "cook_time": "35 dakika",
        "calories": "260 kcal",
        "servings": "4 kişilik",
        "difficulty": "Kolay",
        "score": 94,
        "ingredients": """1 litre süt
1 çay bardağı pirinç
1 su bardağı şeker
2 su bardağı su
1 yemek kaşığı nişasta
1 paket vanilin""",
        "steps": """Pirinci yıkayıp suyla yumuşayana kadar haşlayın.
Sütü ekleyip karıştırarak kaynatın.
Şeker ve vanilini ilave edin.
Nişastayı az suyla açıp tencereye ekleyin.
Kıvam alınca kaselere paylaştırın.
Soğuyunca servis edin.""",
        "tips": "Sütlacı kısık ateşte karıştırarak pişirmek daha pürüzsüz kıvam verir.",
        "serving_suggestion": "Üzerine tarçın serpip soğuk servis edebilirsiniz.",
    },
    {
        "category": "Tatlılar",
        "title": "Islak Kek",
        "description": "Bol soslu, yumuşak dokulu ve pratik çikolatalı kek.",
        "image": "https://images.unsplash.com/photo-1606890737304-57a1ca8a5b62?auto=format&fit=crop&w=900&q=80",
        "time": "50 dakika",
        "prep_time": "15 dakika",
        "cook_time": "35 dakika",
        "calories": "410 kcal",
        "servings": "6 kişilik",
        "difficulty": "Kolay",
        "score": 96,
        "ingredients": """3 adet yumurta
1 su bardağı şeker
1 su bardağı süt
1 su bardağı sıvı yağ
2 yemek kaşığı kakao
1 paket kabartma tozu
1 paket vanilin
2 su bardağı un""",
        "steps": """Yumurta ve şekeri köpürene kadar çırpın.
Süt, sıvı yağ ve kakaoyu ekleyin.
Un, kabartma tozu ve vanilini ilave edin.
Karışımı yağlanmış kalıba dökün.
Önceden ısıtılmış 180 derece fırında pişirin.
Keki fırından çıkarınca sosunu döküp dinlendirin.""",
        "tips": "Sosu kek sıcakken dökerseniz daha iyi içine çeker.",
        "serving_suggestion": "Hindistan cevizi veya çilekle servis edebilirsiniz.",
    },
    {
        "category": "İçecekler",
        "title": "Ev Yapımı Limonata",
        "description": "Taze limon, şeker ve nane ile hazırlanan ferahlatıcı içecek.",
        "image": "https://images.unsplash.com/photo-1621263764928-df1444c5e859?auto=format&fit=crop&w=900&q=80",
        "time": "20 dakika",
        "prep_time": "20 dakika",
        "cook_time": "0 dakika",
        "calories": "120 kcal",
        "servings": "4 kişilik",
        "difficulty": "Kolay",
        "score": 95,
        "ingredients": """4 adet limon
1 su bardağı şeker
1 litre soğuk su
8-10 yaprak nane
Buz""",
        "steps": """Limon kabuklarını rendeleyin.
Limon suyunu sıkın.
Şeker, limon kabuğu ve limon suyunu karıştırın.
Soğuk suyu ekleyip süzün.
Nane ve buzla servis edin.""",
        "tips": "Limon kabuklarını beyaz kısmına kadar rendelemeyin, acılık verebilir.",
        "serving_suggestion": "Bol buz ve taze nane ile servis edin.",
    },
    {
        "category": "İçecekler",
        "title": "Soğuk Kahve",
        "description": "Kahve, süt ve buzla hazırlanan pratik yaz içeceği.",
        "image": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=900&q=80",
        "time": "10 dakika",
        "prep_time": "10 dakika",
        "cook_time": "0 dakika",
        "calories": "180 kcal",
        "servings": "1 kişilik",
        "difficulty": "Kolay",
        "score": 93,
        "ingredients": """1 su bardağı soğuk süt
1 tatlı kaşığı granül kahve
1 tatlı kaşığı şeker
Yarım su bardağı buz
İsteğe bağlı çikolata sosu""",
        "steps": """Kahve ve şekeri az sıcak suyla çözdürün.
Bardağa buzları ekleyin.
Üzerine soğuk sütü dökün.
Kahve karışımını ekleyip karıştırın.
İsteğe bağlı çikolata sosu ile servis edin.""",
        "tips": "Daha köpüklü olması için kahveyi blenderdan geçirebilirsiniz.",
        "serving_suggestion": "Uzun bardakta buzla servis edin.",
    },
    {
        "category": "Tuzlu Yiyecekler",
        "title": "Tuzlu Kurabiye",
        "description": "Ağızda dağılan, çay saatlerine uygun klasik tuzlu kurabiye.",
        "image": "https://images.unsplash.com/photo-1590080876477-91552528d83d?auto=format&fit=crop&w=900&q=80",
        "time": "35 dakika",
        "prep_time": "15 dakika",
        "cook_time": "20 dakika",
        "calories": "320 kcal",
        "servings": "6 kişilik",
        "difficulty": "Kolay",
        "score": 92,
        "ingredients": """125 gr tereyağı
1 çay bardağı sıvı yağ
1 adet yumurta akı
1 yemek kaşığı sirke
1 tatlı kaşığı tuz
1 tatlı kaşığı şeker
1 paket kabartma tozu
Aldığı kadar un
Susam veya çörek otu""",
        "steps": """Tereyağı, sıvı yağ, yumurta akı, sirke, tuz ve şekeri karıştırın.
Kabartma tozu ve unu azar azar ekleyin.
Ele yapışmayan yumuşak hamur yoğurun.
Hamura şekil verip tepsiye dizin.
Üzerine yumurta sarısı sürüp susam serpin.
180 derece fırında kızarana kadar pişirin.""",
        "tips": "Sirke kurabiyenin daha kıyır kıyır olmasını sağlar.",
        "serving_suggestion": "Çay yanında servis edebilirsiniz.",
    },
    {
        "category": "Tuzlu Yiyecekler",
        "title": "Peynirli Poğaça",
        "description": "Yumuşak hamurlu, peynir dolgulu pratik tuzlu atıştırmalık.",
        "image": "https://images.unsplash.com/photo-1608198093002-ad4e005484ec?auto=format&fit=crop&w=900&q=80",
        "time": "55 dakika",
        "prep_time": "25 dakika",
        "cook_time": "30 dakika",
        "calories": "360 kcal",
        "servings": "8 kişilik",
        "difficulty": "Orta",
        "score": 91,
        "ingredients": """1 su bardağı yoğurt
1 çay bardağı sıvı yağ
1 adet yumurta
1 paket kabartma tozu
1 tatlı kaşığı tuz
Aldığı kadar un
Beyaz peynir
Maydanoz""",
        "steps": """Yoğurt, sıvı yağ, yumurta ve tuzu karıştırın.
Kabartma tozu ve unu azar azar ekleyin.
Yumuşak bir hamur yoğurun.
Peynir ve maydanozu karıştırın.
Hamurdan parçalar alıp iç harç koyun.
Üzerine yumurta sarısı sürüp fırında pişirin.""",
        "tips": "Hamuru çok sert yapmayın, poğaça kuru olabilir.",
        "serving_suggestion": "Sıcak veya ılık olarak servis edebilirsiniz.",
    },
]


class Command(BaseCommand):
    help = "ChefAlgo için yerel Türkçe örnek tarifleri veritabanına ekler."

    def handle(self, *args, **options):
        saved_count = 0

        for item in RECIPES:
            category, _ = Category.objects.get_or_create(
                name=item["category"],
                defaults={"icon": "bi-basket"}
            )

            slug = slugify(item["title"].replace("ı", "i"))

            Recipe.objects.update_or_create(
                slug=slug,
                defaults={
                    "category": category,
                    "title": item["title"],
                    "description": item["description"],
                    "image": item["image"],
                    "time": item["time"],
                    "prep_time": item["prep_time"],
                    "cook_time": item["cook_time"],
                    "calories": item["calories"],
                    "servings": item["servings"],
                    "difficulty": item["difficulty"],
                    "score": item["score"],
                    "ingredients": item["ingredients"],
                    "steps": item["steps"],
                    "tips": item["tips"],
                    "serving_suggestion": item["serving_suggestion"],
                }
            )

            saved_count += 1

        self.stdout.write(self.style.SUCCESS(f"{saved_count} yerel tarif başarıyla eklendi/güncellendi."))