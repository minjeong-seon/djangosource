from django.shortcuts import render, get_object_or_404
from ..models import Question
from django.core.paginator import Paginator


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
