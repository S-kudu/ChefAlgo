from django.db import models
from django.contrib.auth.models import User
import random

class Profile(models.Model):
    # Her kullanıcının bir profili olur
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # 6 haneli aktivasyon kodu burada saklanacak
    activation_code = models.CharField(max_length=6, blank=True, null=True)
    
    # Kodun doğrulanıp doğrulanmadığını takip edelim
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Profili"

    # Yeni bir kod üretmek için yardımcı fonksiyon
    def generate_otp(self):
        code = str(random.randint(100000, 999999))
        self.activation_code = code
        self.save()
        return code
    

    
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField()
    prep_time = models.IntegerField(default=0)
    difficulty = models.CharField(max_length=50)
    calories = models.IntegerField()

    def __str__(self):
        return self.title