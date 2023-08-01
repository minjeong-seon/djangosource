from django.shortcuts import render, get_object_or_404
from ..models import Question, QuestionCount
from django.core.paginator import Paginator

# 필터링 여러 조건 한번에 걸어야 할 때 사용하는 함수: Q
from django.db.models import Q, Count
from tools.utils import get_client_ip

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
    # http://127.0.0.1:8000/board/?keyword=검색어&page=1&sort=정렬기준
    # page = request.GET['page']
    page = request.GET.get("page", 1)  # 페이지 정보가 안 들어오면 default = 1로 설정
    keyword = request.GET.get("keyword", "")
    sort = request.GET.get("sort", "recent")

    # select * from question
    # question_list = Question.objects.all()

    # select * from question order by regdate(최신순)
    # select * from question order by (select count(user_id) from question_voter)(추천순)
    # select * from question order by (select count(answer) from question)(인기순)

    if sort == "recommend":
        question_list = Question.objects.annotate(num_voter=Count("voter")).order_by(
            "-num_voter", "-regdate"
        )

    elif sort == "popular":
        question_list = Question.objects.annotate(num_answer=Count("answer")).order_by(
            "-num_answer", "-regdate"
        )
    else:
        question_list = Question.objects.order_by("-regdate")

    # 전체 리스트에서 검색어를 기준으로 필터링 하기
    # 필터링 기준 : 제목, 내용, 질문작성자, 답변작성자
    # __contains : 대소문자 구분  __icontains : 대소문자 구분X
    if keyword:
        question_list = question_list.filter(
            Q(subject__icontains=keyword)
            | Q(content__icontains=keyword)
            | Q(author__username__icontains=keyword)
            | Q(answer__author__username__icontains=keyword)
        ).distinct()

    paginator = Paginator(question_list, 10)
    # paginator 객체에 사용자가 요청한 페이지 정보 담기
    page_obj = paginator.get_page(page)

    context = {
        "question_list": page_obj,
        "page": page,
        "keyword": keyword,
        "sort": sort,
    }

    return render(request, "board/question_list.html", context)


# 질문 상세보기
def question_detail(request, qid):
    page = request.GET.get("page", 1)
    keyword = request.GET.get("keyword")
    sort = request.GET.get("sort")

    question = get_object_or_404(Question, id=qid)

    # 조회수 증가
    # client ip 가져오기
    ip = get_client_ip(request)

    cnt = QuestionCount.objects.filter(ip=ip, question=question).count()

    if cnt == 0:
        # QuestionCount 테이블에 ip와 question 추가
        qc = QuestionCount(ip=ip, question=question)
        qc.save()
        # Question 테이블에 조회수 증가
        if question.view_count:
            question.view_count += 1
        else:
            question.view_count = 1
        question.save()

    context = {
        "question": question,
        "page": page,
        "keyword": keyword,
        "sort": sort,
    }

    return render(request, "board/question_detail.html", context)
