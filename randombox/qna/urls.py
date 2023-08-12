from django.urls import path
from .views.base_view import index, question_detail
from .views.question_views import question_create, question_delete
from .views.answer_views import answer_edit, answer_create, answer_delete

app_name = "qna"

urlpatterns = [
    # http://127.0.0.1:8000/qna/
    path("", index, name="index"),
    # http://127.0.0.1:8000/qna/1/ 상세조회
    path("<int:qid>/", question_detail, name="detail"),
    # http://127.0.0.1:8000/qna/question/create/ 질문등록
    path("question/create/", question_create, name="question_create"),
    # http://127.0.0.1:8000/qna/question/delete/1/ 질문삭제
    path("question/delete/<int:qid>/", question_delete, name="question_delete"),
    # 답변 #
    # http://127.0.0.1:8000/qna/answer/create/질문번호/ -답변 등록
    path("answer/create/<int:qid>/", answer_create, name="answer_create"),
    # http://127.0.0.1:8000/qna/answer/modify/답변번호/질문번호/ -답변 수정
    path("answer/modify/<int:aid>/<int:qid>/", answer_edit, name="answer_edit"),
    # http://127.0.0.1:8000/qna/answer/delete/답변번호/ -답변 삭제
    path("answer/delete/<int:aid>/", answer_delete, name="answer_delete"),
]
