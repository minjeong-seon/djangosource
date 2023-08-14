from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from .forms import UserForm
from randombox.utils import common_data
from randombox.models import Sales, Brand
from django.core.paginator import Paginator
from django.db.models import Q

# 데이터 무작위 추출 함수
from random import choices, choice

# 디렉토리 --> Json 데이터로 반환
from django.http import JsonResponse


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # 회원가입 후 user가 로그인 직접 하기
            # return redirect("users:login")

            # 회원가입 후 로그인 처리 해주기
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # 세션에 정보가 담기게 됨
                login(request, user)
                return redirect("random:main")
    else:
        form = UserForm()
    return render(request, "users/register.html", {"form": form})


# 상품 구매 시 DB 반영 및 자동화: 매출변화, 랜덤가챠, 메일 발송
@login_required(login_url="users:login")
def paid_amount(request):
    user = request.user

    if request.method == "POST":
        new_amount = int(request.POST.get("new_amount", 0))
        buy_amount = new_amount // 20000
        print("구매 버튼 클릭 시 수량: ", buy_amount)

        if new_amount > 0:
            current = user.p_amount + new_amount
            user.p_amount = min(current, 100000)
            user.save()

        cc = common_data(user)

        # 일반 상품에 당첨되지 않은 유저 중 랜덤박스 구매 유저 무작위 1명 추출
        filtered_users = [
            customer
            for customer in cc["user_list"]
            if customer.p_amount > 0 and customer.general.count() < 5
        ]

        if filtered_users:
            print("filtered_users가 비어 있지 않음")
        else:
            print("filtered_users가 비어 있음")

        print("브랜드 최저가: ", cc["min_brand_price"])

        # 남은 매출 초기화
        r = Sales.objects.first()
        r.remain_sales = cc["remain_sales"]
        print("함수 실행 전 남은 매출: ", r.remain_sales)

        # 남은 매출 >= 브랜드 최저가 : 브랜드 재고 감소 & 랜덤유저.brand_id 데이터 삽입
        if r.remain_sales >= cc["min_brand_price"]:
            print("브랜드상품 함수 실행")
            cc["remain_sales"] -= cc["min_brand_price"]
            # 남은 매출 업데이트 객체
            r.remain_sales = cc["remain_sales"]
            r.save()

            print("남은 매출: ", cc["remain_sales"])
            print("총매출: ", cc["total_sales"])

            if filtered_users:
                random_user = choice(filtered_users)
                print("랜덤 유저: ", random_user)

                for brand in cc["brand_list"]:
                    if brand.price == cc["min_brand_price"]:
                        random_user.brand_id = brand.id
                        print("브랜드 당첨자 상품 목록: ", random_user.brand_id)
                        random_user.save()
                        brand.stock_qty = max(brand.stock_qty - 1, 0)
                        brand.save()
                        cc["reduced_stock_qty"] = brand.stock_qty

                        # 당첨 이메일 발송
                        reply_email = EmailMessage(
                            "🎊명품 랜덤박스 당첨 안내🎊",
                            f"안녕하세요. {random_user.username} 님, 랜덤박스 당첨을 축하합니다!🎉 \n\n당첨되신 상품은 메일 수신일로부터 3일 이내 발송 예정입니다.\n\n구매상품: {brand.pname}",
                            to=[random_user.email],
                        )

                        reply_email.send()

                        break

        # 남은 매출 < 브랜드 최저가 : 랜덤일반 재고 감소 & 로그인유저.general 데이터 삽입
        elif cc["remain_sales"] < cc["min_brand_price"]:
            print("일반상품 함수 실행")
            r.remain_sales += new_amount
            r.save()
            # 일반 상품 무작위 추출(구매수량만큼)
            random_generals = choices(cc["general_list"], k=buy_amount)
            for idx, item in enumerate(random_generals):
                print(f"랜덤 상품 목록 {idx+1}:", item)

            print("총매출: ", cc["total_sales"])
            print("남은 매출: ", cc["remain_sales"])

            for random_item in random_generals:
                user.general.add(random_item.id)
                print("랜덤 상품 아이디: ", random_item.id)
                for general in cc["general_list"]:
                    if general.id == random_item.id:
                        general.stock_qty = max(general.stock_qty - 1, 0)
                        general.save()
                        cc["reduced_stock_qty"] = general.stock_qty
                        break

        return render(
            request,
            "event/event_main.html",
        )
    return JsonResponse({"success": False})


# 구매 고객 확인
def customer(request):
    user = request.user
    cc = common_data(user)

    page = request.GET.get("page", 1)
    keyword = request.GET.get("keyword", "")
    sort = request.GET.get("sort", "customer_no")

    users = cc["user_list"]

    if sort == "win":
        users = cc["win_user"]
    elif sort == "not_win":
        users = cc["not_win_user"]
    else:
        users

    if keyword:
        users = users.filter(
            Q(username__icontains=keyword) | Q(email__icontains=keyword)
        ).distinct()

    paginator = Paginator(users, 10)
    page_obj = paginator.get_page(page)

    context = {
        **cc,
        "users": page_obj,
        "page": page,
        "sort": sort,
    }

    return render(request, "users/customer.html", context)
