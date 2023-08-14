from django.shortcuts import render, get_object_or_404
from qna.models import Question

from django.core.paginator import Paginator

# 필터링 여러 조건 한번에 걸어야 할 때 사용하는 함수: Q
from django.db.models import Q, Count


# 질문 목록
def index(request):
    # 사용자가 요청한 페이지 가져오기
    # http://127.0.0.1:8000/board/?keyword=검색어&page=1&sort=정렬기준
    # page = request.GET['page']
    page = request.GET.get("page", 1)  # 페이지 정보가 안 들어오면 default = 1로 설정
    keyword = request.GET.get("keyword", "")
    sort = request.GET.get("sort", "recent")
    question_list = Question.objects.order_by("-regdate")
    # 전체 리스트에서 검색어를 기준으로 필터링 하기
    # 필터링 기준 : 제목, 내용, 질문작성자, 답변작성자
    # __contains : 대소문자 구분  __icontains : 대소문자 구분X
    if keyword:
        question_list = question_list.filter(
            Q(title__icontains=keyword)
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

    return render(request, "qna/question_list.html", context)


# 질문 상세보기
def question_detail(request, qid):
    page = request.GET.get("page", 1)
    keyword = request.GET.get("keyword")
    sort = request.GET.get("sort")

    question = get_object_or_404(Question, id=qid)

    context = {
        "question": question,
        "page": page,
        "keyword": keyword,
        "sort": sort,
    }

    return render(request, "qna/question_detail.html", context)
