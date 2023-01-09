from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import (
    CustomUserCreationForm,
    ProfileForm,
    CustomUserChangeForm,
    CustomAuthenticationForm,
)

from django.http import JsonResponse


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:login")
    else:
        form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "accounts/signup.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("accounts:index")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "accounts/login.html", context)


def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()

            # 만약 이미지가 하나 더 있으면? 첫번째거를 지우고 추가
            if user.profile_set.all().count() > 1:
                user.profile_set.all()[0].delete()

            return redirect("accounts:detail", pk)
    else:
        profile_form = ProfileForm()

    if user.profile_set.all().count() == 0:
        profile_image = None
    else:
        profile_image = user.profile_set.all()[0]
    context = {
        "user": user,
        "profile_form": profile_form,
        "profile_image": profile_image,
    }
    return render(request, "accounts/detail.html", context)


def logout(request):
    auth_logout(request)
    return redirect("/")


# 회원 탈퇴
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)

    return redirect("/")
