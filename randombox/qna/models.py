from django.db import models
from django.contrib.auth import get_user_model


# QNA 게시판
# Question Table
# PK, subject, content, regdate, updatedate
class Question(models.Model):
    author = models.ForeignKey(
        get_user_model(),  # 커스텀 User 모델 가져오기
        on_delete=models.CASCADE,
        related_name="author_question",
    )
    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    regdate = models.DateTimeField(auto_now_add=True, verbose_name="작성날짜")

    # Question 모델 객체를 문자열로 표현할 때 --> 해당 객체의 title 필드 값을 반환
    # 관리자페이지에서 테이블 편하게 보려고 작성(안 하면 주소값 나옴)
    def __str__(self):
        return self.title


# Answer Table
# PK, FK, content, regdate, updatedate
class Answer(models.Model):
    # ForeignKey(연결할 모델 클래스, 자식레코드 삭제 시 부모키 함께 삭제)
    # question = Question 객체 title 필드(칼럼) 값(str)을 FK로 받음
    author = models.ForeignKey(
        get_user_model(),  # 커스텀 User 모델 가져오기
        on_delete=models.CASCADE,
        related_name="author_answer",
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="내용")
    regdate = models.DateTimeField(auto_now_add=True, verbose_name="작성날짜")
    updatedate = models.DateTimeField(verbose_name="수정날짜", null=True, blank=True)
