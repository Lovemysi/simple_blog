from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add_post", views.add_post, name="add_post"),
    path("post/<str:post_id>", views.show_post, name="post"),
    path("update_post/<str:post_id>", views.update_post, name="update_post"),
    path("delete_post/<str:post_id>", views.delete_post, name="delete_post"),
    path("add_comment/<str:post_id>", views.add_comment, name="add_comment"),
]
