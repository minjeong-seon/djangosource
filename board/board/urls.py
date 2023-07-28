from django.urls import path
from .views import (
    index,
    question_detail,
    answer_create,
    question_create,
    question_edit,
    question_delete,
    answer_edit,
    answer_delete,
)

app_name = "board"

urlpatterns = [
    # http://127.0.0.1:8000/board/
    path("", index, name="index"),
    # http://127.0.0.1:8000/board/1/ 상세조회
    path("<int:qid>/", question_detail, name="detail"),
    # http://127.0.0.1:8000/board/question/create/ 질문등록
    path("question/create/", question_create, name="question_create"),
    # http://127.0.0.1:8000/board/question/modify/1/ 질문수정
    path("question/modify/<int:qid>/", question_edit, name="question_edit"),
    # http://127.0.0.1:8000/board/question/delete/1/ 질문삭제
    path("question/delete/<int:qid>/", question_delete, name="question_delete"),
    # 답변 #
    # http://127.0.0.1:8000/board/answer/create/질문번호/ -답변 등록
    path("answer/create/<int:qid>/", answer_create, name="answer_create"),
    # http://127.0.0.1:8000/board/answer/modify/답변번호/질문번호/ -답변 수정
    path("answer/modify/<int:aid>/<int:qid>/", answer_edit, name="answer_edit"),
    # http://127.0.0.1:8000/board/answer/delete/답변번호/ -답변 삭제
    path("answer/delete/<int:aid>/", answer_delete, name="answer_delete"),
]
