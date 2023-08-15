from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from .forms import UserForm
from randombox.utils import common_data
from randombox.models import Sales
from django.core.paginator import Paginator
from django.db.models import Q

# 데이터 무작위 추출 함수
from random import choices, choice

# 디렉토리 --> Json 데이터로 반환
from django.http import JsonResponse

from django.contrib.auth.views import LoginView
from .forms import UserForm


from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm  


# 커스텀 유저용 로그인뷰 사용
class CustomLoginView(LoginView):
    form_class = AuthenticationForm  # AuthenticationForm을 사용
    template_name = 'users/login.html'


# 회원가입 함수
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
    # 로그인 유저 정보 담기
    user = request.user

    if request.method == "POST":
        # 유저가 템플릿에서 전달한 구매금액 가져오기
        new_amount = int(request.POST.get("new_amount", 0))
        buy_amount = new_amount // 20000

        print("구매 버튼 클릭 시 수량: ", buy_amount)

        # 유저 구매 시 : 구매금액 필드값 업데이트
        if new_amount > 0:
            current = user.p_amount + new_amount
            user.p_amount = min(current, 100000)
            user.save()

        cc = common_data(user)

        int_cc_remain = cc["remain_sales"].remain_sales
        cc_obj = Sales.objects.get(remain_sales=int_cc_remain)

        print("브랜드 최저가: ", cc["min_brand_price"])
        print("함수 실행 전 남은 매출DB: ", int_cc_remain ," | ", cc_obj.remain_sales)
        

        # 남은 매출 >= 브랜드 최저가 : 브랜드 재고 감소 & 랜덤유저.brand_id 데이터 삽입
        if int_cc_remain >= cc["min_brand_price"]:
            print("브랜드상품 함수 실행")
            # 남은 매출 - 브랜드 최저가() ==> 필드값 업데이트
            int_cc_remain -= cc["min_brand_price"]
            cc_obj.remain_sales = int_cc_remain
            cc_obj.save()

            print("총매출: ", cc["total_sales"])
            print("당첨 후 남은 매출: ", int_cc_remain,"|",cc_obj.remain_sales)

            # 로그인 유저가 당첨된 일반상품이 구매 수량보다 적은 경우를 필터링
            if user.p_amount > 0 and user.general.count() < buy_amount:
                print("당첨 유저 확인: ", user)

                # 브랜드.가격 필드값이 브랜드 최저가와 일치하면:
                for brand in cc["brand_list"]:
                    if brand.price == cc["min_brand_price"]:
                        # 유저 정보에 해당 데이터 업뎃
                        user.brand_id = brand.id
                        user.save()
                        print("브랜드 당첨자 상품 목록: ", user.brand_id)

                        # 해당 데이터 재고수량 감소(최소값 == 0)
                        brand.stock_qty = max(brand.stock_qty - 1, 0)
                        brand.save()
                        print("당첨 후 해당 상품 재고 수량: ", brand.stock_qty)

                        # 당첨자 이메일 발송
                        reply_email = EmailMessage(
                            "🎊명품 랜덤박스 당첨 안내🎊",
                            f"안녕하세요. {user.username} 님, 랜덤박스 당첨을 축하합니다!🎉 \n\n당첨되신 상품은 메일 수신일로부터 3일 이내 발송 예정입니다.\n\n구매상품: {brand.pname}",
                            to=[user.email],
                        )
                        reply_email.send()
                        break

        # 남은 매출 < 브랜드 최저가 : 랜덤일반 재고 감소 & 로그인유저.general 데이터 삽입
        elif int_cc_remain < cc["min_brand_price"]:
            print("일반상품 함수 실행")
            
            # 남은 매출 업데이트(기존 금액 + 구매 금액)
            int_cc_remain += new_amount
            cc_obj.remain_sales = int_cc_remain
            cc_obj.save()
            print("남은 매출 업데이트: ",cc_obj.remain_sales,"|",int_cc_remain)

            if int_cc_remain >= cc["min_brand_price"]:
                print("당첨하러 돌아갑니다.")
                process_remaining_sales(int_cc_remain, cc_obj, cc, user, buy_amount)
            else:
                # 일반 상품 무작위 추출(구매수량만큼)
                random_generals = choices(cc["general_list"], k=buy_amount)
                for idx, item in enumerate(random_generals):    # --> 콘솔에 찍어보려고 요란하게 함
                    print(f"랜덤 상품 목록 {idx+1}:", item)

                print("총매출: ", cc["total_sales"])
                print("남은 매출: ", int_cc_remain)

                for random_item in random_generals:
                    # 랜덤 추출한 일반 상품 구매 유저 데이터에 업뎃
                    user.general.add(random_item.id)
                    print("랜덤 상품 아이디: ", random_item.id)

                    # 일반 상품 목록 중 랜덤 추출 상품과 일치하는 데이터 재고 감소
                    for general in cc["general_list"]:
                        if general.id == random_item.id:
                            general.stock_qty = max(general.stock_qty - 1, 0)
                            general.save()
                            cc["reduced_stock_qty"] = general.stock_qty
                            break
            
        
        
        # 메인 페이지에서 코드 실행
        return render(
            request,
            "event/event_main.html", cc
        )

    # 관리자 페이지에서도 함수 실행 내용 동적으로 보여줘야 하므로  HttpResponse object 리턴
    return JsonResponse({"success": False}) # 렌더링 실패하면 이거임



# 구매 고객 확인(관리자 페이지 - 구매자 현황 탭)
def customer(request):
    user = request.user
    cc = common_data(user)

    page = request.GET.get("page", 1)
    keyword = request.GET.get("keyword", "")
    sort = request.GET.get("sort", "customer_no")

    users = cc["user_list"]

    # 선택 옵션 별 데이터 분류
    if sort == "win":   # 당첨 유저
        users = cc["win_user"]
    elif sort == "not_win": # 미당첨 유저
        users = cc["not_win_user"]
    else:   # 디폴트: 전체 유저
        users

    # 유저 아이디랑 이메일 범위내에서 검색 가능
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



# paid_amount 함수에서 elif 블록 내부 호출용(브랜드 당첨 함수)
def process_remaining_sales(int_cc_remain, cc_obj, cc, user, buy_amount):
        
        print("함수 실행 전 남은 매출DB: ", int_cc_remain ," | ", cc_obj.remain_sales)

        if int_cc_remain >= cc["min_brand_price"]:
            print("브랜드상품 함수 실행")
            # 남은 매출 - 브랜드 최저가() ==> 필드값 업데이트
            int_cc_remain -= cc["min_brand_price"]
            cc_obj.remain_sales = int_cc_remain
            cc_obj.save()

            print("총매출: ", cc["total_sales"])
            print("당첨 후 남은 매출: ", int_cc_remain,"|",cc_obj.remain_sales)

            # 로그인 유저가 당첨된 일반상품이 구매 수량보다 적은 경우를 필터링
            if user.p_amount > 0 and user.general.count() < buy_amount:
                print("당첨 유저 확인: ", user)

                # 브랜드.가격 필드값이 브랜드 최저가와 일치하면:
                for brand in cc["brand_list"]:
                    if brand.price == cc["min_brand_price"]:
                        # 유저 정보에 해당 데이터 업뎃
                        user.brand_id = brand.id
                        user.save()
                        print("브랜드 당첨자 상품 목록: ", user.brand_id)

                        # 해당 데이터 재고수량 감소(최소값 == 0)
                        brand.stock_qty = max(brand.stock_qty - 1, 0)
                        brand.save()
                        print("당첨 후 해당 상품 재고 수량: ", brand.stock_qty)

                        # 당첨자 이메일 발송
                        reply_email = EmailMessage(
                            "🎊명품 랜덤박스 당첨 안내🎊",
                            f"안녕하세요. {user.username} 님, 랜덤박스 당첨을 축하합니다!🎉 \n\n당첨되신 상품은 메일 수신일로부터 3일 이내 발송 예정입니다.\n\n구매상품: {brand.pname}",
                            to=[user.email],
                        )
                        reply_email.send()
                        break
            return True
        return False