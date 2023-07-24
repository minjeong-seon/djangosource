from django.urls import path
from . import views

urlpatterns = [
    # path(경로, 경로에 응답할 함수, 별칭(옵션))
    # http://127.0.0.1:8000/photo
    path("", views.photo_list, name="photo_list"),
    # http://127.0.0.1:8000/photo/1 (=> photo.id)
    path("<int:id>/", views.photo_detail, name="photo_detail"),
    # http://127.0.0.1:8000/photo/new + get & post
    path("new/", views.photo_add, name="photo_add"),
    # http://127.0.0.1:8000/photo/1/edit + get & post
    path("<int:id>/edit/", views.photo_edit, name="photo_edit"),
    # http://127.0.0.1:8000/photo/1/delete + get
    path("<int:id>/delete/", views.photo_delete, name="photo_delete"),
]
