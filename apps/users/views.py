from django.shortcuts import render, redirect
from django.http import HttpRequest, QueryDict
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDict
from django.core.files.uploadedfile import UploadedFile


from .forms import BlogUserCreationForm, BlogUserHomeForm
from .models import BlogUser


def valid_data(post: QueryDict, keys: list) -> bool:
    for key in post:
        if key not in keys and key != "csrfmiddlewaretoken":
            return False
    return True


# TODO 如果已登录重定向至主页


def register_user(request: HttpRequest):
    form = BlogUserCreationForm()

    if request.method == "POST":
        form = BlogUserCreationForm(request.POST)
        if form.is_valid():
            user: User = form.save()
            blog_user = BlogUser(user=user, username=user.username, email=user.email)
            blog_user.save()
            login(request, user)
            return redirect("home")
        messages.error(request, "Register Failed!")

    if request.user.is_authenticated:  # type: ignore
        blog_user = BlogUser.objects.get(user=request.user)

        return redirect("home")

    return render(request, "users/register.html", {"page_title": "注册", "form": form})


def login_user(request: HttpRequest):
    if request.method == "POST":
        if not valid_data(request.POST, ["username", "password"]):
            messages.error(request, "Bad request!")
            return render(request, "users/login.html", {"page_title": "登录"})

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        messages.error(request, "Username or Password is wrong!")

    if request.user.is_authenticated:
        return redirect("home")

    return render(request, "users/login.html", {"page_title": "登录"})


def logout_user(request: HttpRequest):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def user_home(request: HttpRequest):
    user: User = User.objects.get(pk=request.user.pk)
    blog_user = BlogUser.objects.get(user=request.user)
    form = BlogUserHomeForm(instance=blog_user)

    if request.method == "POST":
        profile_img: UploadedFile | None = request.FILES.get("profile_img")

        if profile_img is not None and valid_data(request.POST, ["username", "email", "profile_img"]):
            blog_user.username = user.username = request.POST["username"]
            blog_user.email = user.email = request.POST["email"]
            blog_user.profile_img.save(profile_img.name, profile_img)
            user.save()
            blog_user.save()
            form = BlogUserHomeForm(instance=blog_user)
            messages.success(request, "修改成功!")

        elif valid_data(request.POST, ["username", "email", "profile_img"]):
            blog_user.username = user.username = request.POST["username"]
            blog_user.email = user.email = request.POST["email"]
            user.save()
            blog_user.save()
            form = BlogUserHomeForm(instance=blog_user)
            messages.success(request, "修改成功!")

        blog_user = BlogUser.objects.get(user=request.user)
        form = BlogUserHomeForm(instance=blog_user)

    return render(request, "users/users_home.html", {"form": form, "page_title": "用户主页", "blog_user": blog_user})
