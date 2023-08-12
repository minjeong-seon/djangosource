from django.shortcuts import render
from .utils import common_data
from qna.models import Question
from .models import Sales

# Paginator(object_list | Count | Ordered)
from django.core.paginator import Paginator


# 홈 - 이벤트 템플릿
# 랜덤박스 모델 데이터, 로그인유저 p_amount 데이터 전달
def main(request):
    login_user = request.user

    cc = common_data(login_user)

    context = {
        **cc,
    }
    return render(request, "event/event_main.html", context)


# 관리자 템플릿 : 총괄 모니터링
# 미답변 질문 개수, 판매수량, 매출 관련 데이터 전달 & 템플릿에서 form data 전달 받아 처리


def master(request):
    login_user = request.user
    cc = common_data(login_user)

    # 답변이 없는 질문 조회
    # select q.* from qna_question as q left join qna_answer as a on q.id = a.question_id where a.id is null;
    waiting_question = Question.objects.filter(answer__isnull=True).order_by("regdate")

    wq_count = waiting_question.count()

    page = request.GET.get("page", 1)
    sort = request.GET.get("sort", "recent")

    paginator = Paginator(waiting_question, 10)
    page_obj = paginator.get_page(page)
    remain = Sales.objects.first()

    context = {
        **cc,
        "page": page,
        "sort": sort,
        "waiting_question": page_obj,
        "wq_count": wq_count,
        "remain": remain.remain_sales,
    }
    return render(request, "users/master.html", context)


# utils.py 에서 넘겨받은 context_data는 딕셔너리 구조
#   ㄴ> views.py 함수 내에서 호출 시 : dict[변수명]
