from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.contrib import messages
from django.core.files.uploadedfile import UploadedFile

from users.models import BlogUser
from .forms import PostForm
from .models import Post, Comment


def home(request: HttpRequest):
    post_list = Post.objects.all()

    if request.user.is_authenticated:  # type: ignore
        blog_user = BlogUser.objects.get(user=request.user)
        return render(request, "posts/posts_index.html", {"page_title": "主页", "blog_user": blog_user, "post_list": post_list})

    return render(request, "posts/posts_index.html", {"page_title": "主页", "post_list": post_list})


@login_required(login_url="login")
def add_post(request: HttpRequest):
    blog_user = BlogUser.objects.get(user=request.user)
    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post: Post = form.save(commit=False)
            post.author = blog_user
            post.save()
            return redirect("home")

    return render(request, "posts/add_post.html", {"page_title": "添加文章", "blog_user": blog_user, "form": form})


def show_post(request: HttpRequest, post_id: str):
    blog_user = None

    if request.user.is_authenticated:  # type: ignore
        blog_user = BlogUser.objects.get(user=request.user)

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return redirect("home")

    comments = Comment.objects.filter(post=post)

    body_paragraphs = str(post.body).split("\n")
    return render(
        request, "posts/post.html", {"page_title": post.title, "post": post, "comments": comments, "body_paragraphs": body_paragraphs, "blog_user": blog_user}
    )


@login_required(login_url="login")
def update_post(request: HttpRequest, post_id: str):
    blog_user = BlogUser.objects.get(user=request.user)

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return redirect("home")

    if post.author.id != blog_user.id:
        messages.error(request, "无权修改文章!")
        return redirect("home")

    form = PostForm(instance=post)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        cover: UploadedFile | None = request.FILES.get("cover")
        if form.is_valid() and cover is not None:
            update_form: Post = form.save(commit=False)
            update_form.cover.save(cover.name, cover)
            update_form.save()
            return redirect("home")
        elif form.is_valid():
            form.save()
            return redirect("home")

    return render(request, "posts/update_post.html", {"page_title": "修改文章", "form": form, "post": post, "blog_user": blog_user})


def delete_post(request: HttpRequest, post_id: str):
    blog_user = BlogUser.objects.get(user=request.user)
    try:
        post = Post.objects.get(pk=post_id)
    except Exception:
        return redirect("home")

    if post.author.id != blog_user.id:
        messages.error(request, "无权修改文章!")
        return redirect("home")

    post.delete()
    messages.success(request, "文章删除成功!")

    return redirect("home")


@login_required(login_url="login")
def add_comment(request: HttpRequest, post_id: str):
    blog_user = BlogUser.objects.get(user=request.user)

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        messages.error(request, "未找到文章")
        return redirect("home")

    if request.method == "POST":
        comment_body = request.POST.get("body")
        if comment_body == None or comment_body == "":
            messages.error(request, "评论无内容")
            return redirect("post", post_id=post_id)

        comment = Comment(author=blog_user, post=post, body=comment_body)
        comment.save()
        messages.success(request, "评论成功!")
        return redirect("post", post_id=post_id)

    body_paragraphs = str(post.body).split("\n")
    return render(request, "posts/post.html", {"page_title": post.title, "post": post, "body_paragraphs": body_paragraphs, "blog_user": blog_user})
