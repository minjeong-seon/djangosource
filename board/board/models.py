from django.db import models
from django.contrib.auth.models import User

# Question, Answer 모델에서 author, voter 2개의 필드가 User 모델을 참조하고 있음
# User.question_set <-- 이 방식으로 Question 모델에 접근 시 어느 필드가 기준인지 알려줘야 함
# 특정 필드에 이름만 부여 해놓기 : related_name


# Question Table
# PK, subject, content, regdate, updatedate
class Question(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_question"
    )
    subject = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    regdate = models.DateTimeField(auto_now_add=True, verbose_name="작성날짜")
    # 수정날짜는 사용자가 직접 넣기 + nullable
    updatedate = models.DateTimeField(verbose_name="수정날짜", null=True, blank=True)

    # 추천 필드
    voter = models.ManyToManyField(User, related_name="voter_question")
    # 조회수
    view_count = models.BigIntegerField(default=0)

    # Question 모델 객체를 문자열로 표현할 때 --> 해당 객체의 subject 필드 값을 반환
    # 관리자페이지에서 테이블 편하게 보려고 작성(안 하면 주소값 나옴)
    def __str__(self) -> str:
        return self.subject


# Answer Table
# PK, FK, content, regdate, updatedate
class Answer(models.Model):
    # ForeignKey(연결할 모델 클래스, 자식레코드 삭제 시 부모키 함께 삭제)
    # question = Question 객체 subject 필드(칼럼) 값(str)을 FK로 받음
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_answer"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="내용")
    regdate = models.DateTimeField(auto_now_add=True, verbose_name="작성날짜")
    updatedate = models.DateTimeField(verbose_name="수정날짜", null=True, blank=True)

    # 추천 필드
    voter = models.ManyToManyField(User, related_name="voter_answer")


# Reply Table
# 질문에 대한 댓글, 답변에 대한 댓글 테이블
# PK(자동생성), author, content, regdate, updatedate, FK(소속이 질문인지 답변인지)
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    content = models.TextField(verbose_name="댓글 내용")
    regdate = models.DateTimeField(auto_now_add=True, verbose_name="작성날짜")
    updatedate = models.DateTimeField(verbose_name="수정날짜", null=True, blank=True)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, null=True, blank=True
    )
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)


class QuestionCount(models.Model):
    """
    조회수 업데이트를 위한 모델
    사용자의 ip 저장
    """

    ip = models.CharField(max_length=30)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.ip
