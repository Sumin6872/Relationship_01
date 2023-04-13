from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserSignupForm, CustomUserSigninForm
from .models import CustomUser, Profile


def signup(request):
    form = CustomUserSignupForm()
    if request.method == "POST":
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    return render(request, "newSignup.html", {"form": form})


def signin(request):
    form = CustomUserSigninForm()
    if request.method == 'POST':
        form = CustomUserSigninForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
    return render(request, "newSignin.html", {"form": form})


def signout(request):
    logout(request)
    return redirect("home")


def new_profile(request):
    if request.user.is_anonymous:
        return redirect('home')
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'newProfile.html', {"profile":profile})


def create_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.nickname = request.POST.get('nickname')
        profile.image = request.FILES.get('image')
        profile.save()
        return redirect('users:new_profile')

    return render(request, 'newProfile.html', {'profile': profile})
