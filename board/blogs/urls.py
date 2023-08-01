from django.urls import path, include
from .views import (
    post_create,
    post_edit,
    post_delete,
    post_list,
    post_detail,
    post_like,
)

app_name = "blog"

urlpatterns = [
    # http://127.0.0.1:8000/post/
    path("", post_list, name="post_list"),
    # http://127.0.0.1:8000/post/create/
    path("create/", post_create, name="post_create"),
    # http://127.0.0.1:8000/post/detail/번호/
    path("detail/<int:post_id>/", post_detail, name="post_detail"),
    # http://127.0.0.1:8000/post/edit/번호/
    path("edit/<int:post_id>/", post_edit, name="post_edit"),
    # http://127.0.0.1:8000/post/delete/번호/
    path("delete/<int:post_id>/", post_delete, name="post_delete"),
    # http://127.0.0.1:8000/post/likes/번호/
    path("likes/<int:post_id>/", post_like, name="post_like"),
]
