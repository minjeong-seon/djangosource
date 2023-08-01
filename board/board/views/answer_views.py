from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from ..models import Question, Answer
from ..forms import AnswerForm

from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

############## 답변 영역 ###############


@login_required(login_url="users:login")
def answer_create(request, qid):
    """
    답변등록 2가지 방법
    1) question 객체 사용
        question.answer_set.create()

    2) insert into answer values('답변','qid')
        question = get_object_or_404(Question, id=qid)
        answer = Answer(question=question, content=request.POST[''])
        answer.save()
    """
    # form 을 사용하지 않는 방식
    # question = get_object_or_404(Question, id=qid)
    # question.answer_set.create(content=request.POST["content"])

    # form 을 사용하는 방식
    question = get_object_or_404(Question, id=qid)
    if request.method == "POST":
        form = AnswerForm(request.POST)

        if form.is_valid():
            # form.save() : commit = True 가 default임 ==> DB에 바로 반영됨
            answer = form.save(commit=False)
            # 어느 질문에 대한 답변인지 확인 후 DB 저장
            answer.question = question
            answer.author = request.user
            answer.save()
            # return redirect("board:detail", qid=qid)
            # detail 앵커 이용(a태그 name="answer_{}")
            # resolve_url(패턴이름, 위치) : url로 변환
            return redirect(
                "{}#answer_{}".format(resolve_url("board:detail", qid=qid), answer.id)
            )

    else:
        form = AnswerForm()

    context = {"question": question, "form": form}
    return render(request, "board/question_detail.html", context)


@login_required(login_url="users:login")
def answer_edit(request, aid, qid):
    answer = get_object_or_404(Answer, id=aid)
    question = get_object_or_404(Question, id=qid)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.updatedate = timezone.now()
            answer.save()
            return redirect("board:detail", qid=qid)
    else:
        form = AnswerForm(instance=answer)
    return render(
        request,
        "board/answer_edit.html",
        {"question": question, "form": form, "answer": answer},
    )


def answer_delete(request, aid):
    """
    답변 삭제 후 detail 이동
    """
    answer = get_object_or_404(Answer, id=aid)
    answer.delete()

    # qid = answer.question_id(테이블 필드명 이용)
    # qid = answer.question.id
    return redirect("board:detail", qid=answer.question.id)


# 답변 추천
@login_required(login_url="users:login")
def vote_answer(request, aid):
    # 질문 찾기
    answer = get_object_or_404(Answer, id=aid)
    # 이미 추천한 글인지 확인
    if answer.voter.filter(id=request.user.id).exists():
        messages.warning(request, "이미 추천한 글입니다.")
    elif request.user == answer.author:
        messages.error(request, "본인이 작성한 글은 추천하실 수 없습니다.")
    else:
        # 로그인 사용자 != 질문작성자일 때 추천 수 증가 + detail 페이지 이동
        answer.voter.add(request.user)  # 추천 유저 추가
    return redirect("board:detail", qid=answer.question.id)
