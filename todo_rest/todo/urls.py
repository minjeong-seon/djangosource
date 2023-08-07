from django.urls import path
from .views import TodoApiView

urlpatterns = [
    # 클래스로 작성된 view 사용 시 as_view() 사용
    path("", TodoApiView.as_view(), name="todo")
]
