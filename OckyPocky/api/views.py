from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import CreateUserForm


def register(request):
    if request.user.is_authenticated:
        return redirect("profile_page")
    else:
        form = CreateUserForm()

        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get("username")
                messages.success(request, f"Account was created for {username}")

                return redirect("login")

        context = {"form": form}
        return render(request, "api/register.html", context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect("profile_page")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("profile_page")
            else:
                messages.info(request, "Username or password is incorrect.")

        context = {}
        return render(request, "api/login.html", context)


def logout_user(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def profile(request):
    context = {}
    return render(request, "api/profile.html", context)


@login_required(login_url="login")
def update_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect("profile_page")

        form = PasswordChangeForm(user=request.user)
        context = {"form": form}
    return render(request, "api/update_password.html", context)
