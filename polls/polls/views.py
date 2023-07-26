from django.shortcuts import render, get_object_or_404, redirect
from .models import Question


def index(request):
    """
    전체 질문목록 가져오기 - 작성날짜 내림차순
    """
    question_list = Question.objects.order_by("-pub_date")
    return render(request, "polls/index.html", {"question_list": question_list})


def detail(request, question_id):
    # question_id를 이용해 선택사항 가져오기
    # Question과 관련된 Choice는 알아서 따라감
    question = get_object_or_404(Question, id=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    pass


def vote(request, question_id):
    pass
