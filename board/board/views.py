from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required

from django.utils import timezone

"""
페이지 나누기
Paginator 클래스
Paginator(전체리스트, 페이지당 보여줄 개수)

has_previous : 이전 페이지 유무
has_next : 다음 페이지 유무

previous_page_number : 이전 페이지 번호
next_page_number : 다음 페이지 번호
number : 현재 페이지 번호

page_range : 페이지 범위
count : 전체 게시물 개수
start_index : 현재 페이지 인덱스(1~시작)

"""


# 질문 목록
def index(request):
    # 사용자가 요청한 페이지 가져오기
    # http://127.0.0.1:8000/board/?page=1
    # page = request.GET['page']
    page = request.GET.get("page", 1)  # 페이지 정보가 안 들어오면 default = 1로 설정

    # select * from question
    # question_list = Question.objects.all()

    # select * from question order by regdate
    question_list = Question.objects.order_by("-regdate")

    paginator = Paginator(question_list, 10)
    # paginator 객체에 사용자가 요청한 페이지 정보 담기
    page_obj = paginator.get_page(page)

    context = {"question_list": page_obj}

    return render(request, "board/question_list.html", context)


# 질문 상세보기
def question_detail(reqeust, qid):
    question = get_object_or_404(Question, id=qid)

    context = {"question": question}
    return render(reqeust, "board/question_detail.html", context)


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
            return redirect("board:detail", qid=qid)
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
