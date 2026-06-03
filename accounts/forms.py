from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ChefAlgoRegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Ad', max_length=150, required=True)
    last_name = forms.CharField(label='Soyad', max_length=150, required=True)
    email = forms.EmailField(label='E-posta', required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'username': 'Kullanıcı adı',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu e-posta adresi zaten kullanılıyor.')
        return email
