from django.urls import path
from .views.base_views import index, question_detail
from .views.question_views import (
    question_create,
    question_edit,
    question_delete,
    vote_question,
)
from .views.answer_views import answer_edit, answer_create, answer_delete, vote_answer
from .views.comment_views import (
    comment_create_q,
    comment_delete_q,
    comment_edit_q,
    comment_edit_a,
    comment_create_a,
    comment_delete_a,
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
    # 질문댓글
    # http://127.0.0.1:8000/board/comment/create/question/질문번호/ -질문댓글작성
    path(
        "comment/create/question/<int:qid>/", comment_create_q, name="comment_create_q"
    ),
    # http://127.0.0.1:8000/board/comment/edit/question/댓글번호/ -질문댓글수정
    path("comment/edit/question/<int:cid>/", comment_edit_q, name="comment_edit_q"),
    # http://127.0.0.1:8000/board/comment/delete/question/댓글번호/ -질문댓글삭제
    path(
        "comment/delete/question/<int:cid>/", comment_delete_q, name="comment_delete_q"
    ),
    # 답변댓글
    # http://127.0.0.1:8000/board/comment/create/answer/답변번호/ -답변댓글작성
    path("comment/create/answer/<int:aid>/", comment_create_a, name="comment_create_a"),
    # http://127.0.0.1:8000/board/comment/edit/answer/댓글번호/ -답변댓글수정
    path("comment/edit/answer/<int:cid>/", comment_edit_a, name="comment_edit_a"),
    # http://127.0.0.1:8000/board/comment/delete/answer/댓글번호/ -답변댓글삭제
    path("comment/delete/answer/<int:cid>/", comment_delete_a, name="comment_delete_a"),
    # 추천
    # 질문 추천
    path("vote/question/<int:qid>/", vote_question, name="vote_question"),
    # 답변 추천
    path("vote/answer/<int:aid>/", vote_answer, name="vote_answer"),
]
