from django.shortcuts import render, get_object_or_404, redirect
from .models import Question


# 질문 목록 보여주기: select * from question
def index(request):
    """
    전체 질문목록 가져오기 - 작성날짜 내림차순
    """
    question_list = Question.objects.order_by("-pub_date")
    return render(request, "polls/index.html", {"question_list": question_list})


# 질문에 대한 선택사항 보여주기: select ~ from ~ join ~ on
def detail(request, question_id):
    # question_id를 이용해 선택사항 가져오기
    # Question과 관련된 Choice는 알아서 따라감
    question = get_object_or_404(Question, id=question_id)
    return render(request, "polls/detail.html", {"question": question})


# vote 버튼 클릭 시 투표 수 증가: update
def vote(request, question_id):
    # 질문 가져오기
    question = get_object_or_404(Question, id=question_id)

    if request.method == "POST":
        # question의 id를 이용해서 Choice 찾기
        # 방법1: Choice.objects.get(id=뭐뭐)도 가능하지만 objects.get은 id를 못 찾으면 key error 발생
        #   == select * from qeustion where id=뭐뭐
        # 방법2: Choice.objects.filter(id=뭐뭐)는 못 찾으면 비어있는 QuerySet return함(like 랑 비슷)
        # 방법3: choice_set.get(id=뭐뭐) == select * from choice where id=뭐뭐
        try:
            selected_choice = question.choice_set.get(id=request.POST["choice"])
        except KeyError as e:
            return render(request, "polls/detail.html")
        else:
            selected_choice.vote += 1
            selected_choice.save()
            # 투표 성공 후 --> 결과 페이지 이동
            return redirect("results", question_id=question_id)


# 투표 결과 보여주기
def results(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, "polls/results.html", {"question": question})
