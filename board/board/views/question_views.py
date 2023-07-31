from django.shortcuts import render, get_object_or_404, redirect
from ..models import Question
from ..forms import QuestionForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# django 메세지 기능
from django.contrib import messages


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
            return redirect("board:index")
    else:
        form = QuestionForm()

    return render(request, "board/question_create.html", {"form": form})


# 질문 수정(작성자==로그인 사용자일 때)
@login_required(login_url="users:login")
def question_edit(request, qid):
    question = get_object_or_404(Question, id=qid)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)

        if form.is_valid():
            # 수정 날짜 추가
            question = form.save(commit=False)
            question.updatedate = timezone.now()
            question.save()
            return redirect("board:detail", qid=qid)
    else:
        form = QuestionForm(instance=question)

    return render(request, "board/question_edit.html", {"form": form})


# 질문 삭제
@login_required(login_url="users:login")
def question_delete(request, qid):
    # qid로 찾은 질문 삭제 후 리스트로 이동
    question = get_object_or_404(Question, id=qid)
    question.delete()

    return redirect("index")


# 질문 추천
@login_required(login_url="users:login")
def vote_question(request, qid):
    # 질문 찾기
    question = get_object_or_404(Question, id=qid)
    # 이미 추천한 글인지 확인
    if question.voter.filter(id=request.user.id).exists():
        messages.warning(request, "이미 추천한 글입니다.")
    elif request.user == question.author:
        messages.error(request, "본인이 작성한 글은 추천하실 수 없습니다.")
    else:
        # 로그인 사용자 != 질문작성자일 때 추천 수 증가 + detail 페이지 이동
        question.voter.add(request.user)  # 추천 유저 추가
    return redirect("board:detail", qid=qid)
