import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.html import strip_tags

# Modellerini ve Formlarını içe aktar
from dashboard.models import Profile 
from .forms import ChefAlgoRegisterForm

# --- 1. KAYIT GÖRÜNÜMÜ ---
def register_view(request):
    if request.method == 'POST':
        form = ChefAlgoRegisterForm(request.POST)
        if form.is_valid():
            # Kullanıcıyı oluştur ama pasif bırak
            user = form.save(commit=False)
            user.is_active = False 
            user.save()

            # OTP Üret
            otp_code = str(random.randint(100000, 999999))

            # PROFİL GÜNCELLEME (Veritabanına kaydet ki verify okuyabilsin)
            # Profile modelinde 'activation_code' alanı olduğunu varsayıyoruz
            profile, created = Profile.objects.get_or_create(user=user)
            profile.activation_code = otp_code
            profile.save()

            # SESSION YÖNETİMİ
            request.session['pending_user_id'] = user.id
            request.session.set_expiry(600)  # 10 Dakika

            # E-posta İçeriği (Profesyonel HTML)
            subject = f"{otp_code} - ChefAlgo Doğrulama Kodunuz"
            html_message = f"""
            <div style="background-color: #0f172a; padding: 40px; font-family: sans-serif; color: #ffffff; text-align: center; border-radius: 20px;">
                <h1 style="color: #ffffff;">Chef<span style="color: #10b981;">Algo</span></h1>
                <div style="background-color: #111827; padding: 30px; border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; max-width: 400px; margin: 0 auto;">
                    <h2 style="font-size: 20px;">Hoş Geldiniz Şef!</h2>
                    <p style="color: #94a3b8;">Mutfak algoritmanızı başlatmak için doğrulama kodunuz:</p>
                    <div style="background: rgba(16, 185, 129, 0.1); border: 2px dashed #10b981; padding: 20px; margin: 25px 0; border-radius: 12px;">
                        <span style="font-size: 36px; font-weight: bold; letter-spacing: 8px; color: #10b981;">{otp_code}</span>
                    </div>
                </div>
            </div>
            """
            plain_message = strip_tags(html_message)
            
            try:
                send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [user.email], html_message=html_message)
                messages.success(request, "Kayıt başarılı! E-postanızdaki kodu girin.")
                return redirect('accounts:verify_otp')
            except Exception as e:
                print(f"SMTP Hatası: {e}")
                messages.warning(request, "E-posta gönderilemedi ama kaydınız alındı. Kod: " + otp_code)
                return redirect('accounts:verify_otp')
    else:
        form = ChefAlgoRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


# --- 2. DOĞRULAMA GÖRÜNÜMÜ ---
def verify_otp_view(request):
    user_id = request.session.get('pending_user_id')
    
    if not user_id:
        messages.error(request, "Oturum süresi dolmuş veya geçersiz işlem.")
        return redirect('accounts:register')

    if request.method == 'POST':
        otp_entered = request.POST.get('otp_code')
        
        try:
            profile = Profile.objects.get(user_id=user_id)
            if profile.activation_code == otp_entered:
                # Hesabı Aktifleştir
                user = profile.user
                user.is_active = True
                user.save()
                
                # Profilde varsa verified işaretle
                if hasattr(profile, 'is_verified'):
                    profile.is_verified = True
                    profile.save()
                
                # Session temizle
                del request.session['pending_user_id']
                
                messages.success(request, "Hesabınız doğrulandı! Şimdi giriş yapabilirsiniz.")
                return redirect('accounts:login') # İsteğin üzerine Giriş sayfasına yönlendirme
            else:
                messages.error(request, "Girdiğiniz kod hatalı!")
        except Profile.DoesNotExist:
            return redirect('accounts:register')
            
    return render(request, 'accounts/verify_otp.html')


# --- 3. GİRİŞ GÖRÜNÜMÜ ---
def login_view(request):
    # Eğer kullanıcı zaten giriş yapmışsa direkt ana sayfaya gönder
    if request.user.is_authenticated:
        return redirect('dashboard:panel')

    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        
        # Kullanıcıyı doğrula
        user = authenticate(request, username=u_name, password=p_word)

        if user is not None:
            # Kullanıcı hesabı aktif mi? (OTP onayından geçmiş mi?)
            if user.is_active:
                login(request, user)
                
                # --- PROFESYONEL BİLDİRİM ---
                messages.success(
                    request, 
                    f"Hoş geldin Şef {user.username}! Mutfak algoritman başarıyla başlatıldı.",
                    extra_tags='login-success'
                )
                
                # ÖNEMLİ: 'home' ismi dashboard/urls.py içindeki name="home" ile eşleşmeli
                return redirect('dashboard:panel') 
            
            else:
                # Kullanıcı aktif değilse (OTP onaylamadıysa)
                # Session'a kullanıcı ID'sini atıyoruz ki verify sayfasında kimi onayladığımızı bilelim
                request.session['pending_user_id'] = user.id
                messages.warning(request, "Hesabınız henüz onaylanmamış. Lütfen e-postanıza gelen kodu girin.")
                
                # 'accounts:verify_otp' ismi accounts/urls.py içindeki name="verify_otp" ile eşleşmeli
                return redirect('accounts:verify_otp')
        else:
            # Kullanıcı bulunamadıysa veya şifre yanlışsa
            messages.error(request, "Kullanıcı adı veya şifre hatalı. Lütfen bilgilerinizi kontrol edin.")
            
    return render(request, 'accounts/login.html')


# --- 4. ÇIKIŞ GÖRÜNÜMÜ ---
def logout_view(request):
    logout(request)
    messages.info(request, 'Güvenle çıkış yapıldı.')
    return redirect('accounts:home')  # veya 'dashboard:panel'

def home(request):
    return redirect('dashboard:home')