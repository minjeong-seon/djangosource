from django.shortcuts import render, get_object_or_404, redirect
from ..models import Question
from ..forms import QuestionForm
from django.contrib.auth.decorators import login_required


# django 메세지 기능
# from django.contrib import messages


# 질문 등록
@login_required(login_url="users:login")
def question_create(request):
    """
    질문등록
    get --> 비어있는 QuestionForm 보내기
    post --> QuestionForm에 사용자 입력값 담아서 보내기
    """
    if request.method == "POST":
        form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user  # 로그인 사용자 정보를 author 에 담기
            question.save()
            return redirect("qna:index")
    else:
        form = QuestionForm()

    return render(request, "qna/question_create.html", {"form": form})


# 질문 삭제
@login_required(login_url="users:login")
def question_delete(request, qid):
    # qid로 찾은 질문 삭제 후 리스트로 이동
    question = get_object_or_404(Question, id=qid)
    question.delete()

    return redirect("qna:index")
