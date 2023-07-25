from django.urls import path
from . import views

urlpatterns = [
    # http://127.0.0.1:8000/todo/
    path("", views.todo_list, name="todo_list"),
    # http://127.0.0.1:8000/todo/id번호
    # <type:변수명>/
    path("<int:id>/", views.todo_detail, name="todo_detail"),
    # http://127.0.0.1:8000/todo/create
    path("create/", views.todo_create, name="todo_create"),
    # http://127.0.0.1:8000/todo/id번호/edit
    path("<int:id>/edit/", views.todo_edit, name="todo_edit"),
    # http://127.0.0.1:8000/todo/id번호/delete
    path("<int:id>/delete/", views.todo_delete, name="todo_delete"),
    # http://127.0.0.1:8000/todo/done/id번호
    path("done/<int:id>/", views.todo_done, name="todo_done"),
    # http://127.0.0.1:8000/todo/done
    path("done/", views.done_list, name="done_list"),
]
