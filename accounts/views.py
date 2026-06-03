import random
from urllib.parse import urlencode

from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

from .forms import ChefAlgoRegisterForm
from .models import EmailVerificationCode


def generate_code():
    return str(random.randint(100000, 999999))


def newsletter_entry_view(request):
    if request.method != "POST":
        return redirect("home")

    email = request.POST.get("email", "").strip().lower()

    if not email:
        messages.error(request, "Lütfen geçerli bir e-posta adresi girin.")
        return redirect("home")

    query_string = urlencode({"email": email})

    user_exists = User.objects.filter(email__iexact=email).exists()

    if user_exists:
        return redirect(f"{reverse('login')}?{query_string}")

    return redirect(f"{reverse('register')}?{query_string}")

def register_view(request):
    initial_email = request.GET.get("email", "").strip().lower()

    if request.method == "POST":
        form = ChefAlgoRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            code = generate_code()

            EmailVerificationCode.objects.update_or_create(
                user=user,
                defaults={"code": code}
            )

            send_mail(
                subject="ChefAlgo Doğrulama Kodunuz",
                message=(
                    f"Merhaba {user.first_name},\n\n"
                    f"ChefAlgo doğrulama kodunuz: {code}\n\n"
                    "Bu kod 10 dakika geçerlidir."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            request.session["verification_user_id"] = user.id

            request.session["verify_notice"] = (
                "Başarıyla kaydolundu. Mail adresinize gönderilen kodu girin."
            )

            return redirect("verify_email")
    else:
        form = ChefAlgoRegisterForm(initial={
            "email": initial_email
        })

    return render(request, "accounts/register.html", {
        "form": form
    })


def verify_email_view(request):
    user_id = request.session.get("verification_user_id")

    if not user_id:
        messages.error(request, "Doğrulama işlemi bulunamadı. Lütfen tekrar kayıt olun.")
        return redirect("register")

    try:
        user = User.objects.get(id=user_id)
        verification = EmailVerificationCode.objects.get(user=user)
    except (User.DoesNotExist, EmailVerificationCode.DoesNotExist):
        messages.error(request, "Doğrulama kodu bulunamadı.")
        return redirect("register")

    if request.method == "POST":
        entered_code = request.POST.get("code", "").strip()

        if verification.is_expired():
            verification.delete()
            user.delete()
            request.session.pop("verification_user_id", None)
            request.session.pop("verify_notice", None)

            messages.error(
                request,
                "Doğrulama kodunun süresi doldu. Lütfen tekrar kayıt olun."
            )
            return redirect("register")

        if entered_code == verification.code:
            user.is_active = True
            user.save()

            verification.delete()

            request.session.pop("verification_user_id", None)
            request.session.pop("verify_notice", None)

            login(request, user)

            messages.success(request, "Başarıyla giriş yapıldı.")
            return redirect("dashboard")

        messages.error(request, "Doğrulama kodu hatalı.")

    verify_notice = request.session.get(
        "verify_notice",
        "Mail adresinize gönderilen doğrulama kodunu girin."
    )

    return render(request, "accounts/verify_email.html", {
        "hide_navbar": True,
        "hide_footer": True,
        "verify_notice": verify_notice,
    })

def resend_verification_code_view(request):
    if request.method != "POST":
        return redirect("verify_email")

    user_id = request.session.get("verification_user_id")

    if not user_id:
        messages.error(request, "Doğrulama işlemi bulunamadı. Lütfen tekrar kayıt olun.")
        return redirect("register")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "Kullanıcı bulunamadı. Lütfen tekrar kayıt olun.")
        return redirect("register")

    code = generate_code()

    EmailVerificationCode.objects.update_or_create(
        user=user,
        defaults={"code": code}
    )

    send_mail(
        subject="ChefAlgo Yeni Doğrulama Kodunuz",
        message=(
            f"Merhaba {user.first_name},\n\n"
            f"Yeni ChefAlgo doğrulama kodunuz: {code}\n\n"
            "Bu kod 10 dakika geçerlidir."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

    request.session["verify_notice"] = (
        "Yeni doğrulama kodu mail adresinize gönderildi."
    )

    return redirect("verify_email")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    initial_email = request.GET.get("email", "").strip().lower()

    if request.method == "POST":
        post_data = request.POST.copy()
        username_or_email = post_data.get("username", "").strip()

        if "@" in username_or_email:
            users = User.objects.filter(email__iexact=username_or_email)

            if users.exists():
                active_user = users.filter(is_active=True).first()
                selected_user = active_user if active_user else users.first()
                post_data["username"] = selected_user.username

        form = AuthenticationForm(request, data=post_data)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request, "Başarıyla giriş yapıldı.")
            return redirect("dashboard")

        messages.error(request, "Kullanıcı adı, e-posta veya şifre hatalı.")
    else:
        form = AuthenticationForm(initial={
            "username": initial_email
        })

    return render(request, "accounts/login.html", {
        "form": form
    })


def logout_view(request):
    logout(request)
    messages.info(request, "Oturum güvenli bir şekilde kapatıldı.")
    return redirect("home")