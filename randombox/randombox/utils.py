from .models import General, Brand, Sales
from users.models import CustomUser

# Paginator(object_list | Count | Ordered)
# from django.core.paginator import Paginator

# ORM 데이터 필드값 합계 함수
from django.db.models import Sum

# 데이터 무작위 추출 함수
from random import choices, choice


def common_data(login_user):
    general_all = General.objects.all()
    general_list = General.objects.exclude(stock_qty=0)
    brand_all = Brand.objects.all()
    brand_list = Brand.objects.exclude(stock_qty=0)
    # brand_id 필드값이 존재하는 데이터만 가져오기
    win_user = CustomUser.objects.filter(brand_id__isnull=False)
    # brand_id 필드값이 존재하지 않는 데이터만 가져오기
    not_win_user = CustomUser.objects.filter(brand_id__isnull=True, p_amount__gt=0)

    if login_user.is_authenticated:
        user_list = CustomUser.objects.order_by("id")

        # CustomUser 모델의 p_amount 필드 값의 합계를 계산
        total_sales = CustomUser.objects.aggregate(total=Sum("p_amount"))["total"] or 0

        # General 모델의 stock_qty 필드 값의 합계를 계산
        g_stock = General.objects.aggregate(total_stock=Sum("stock_qty"))["total_stock"]

        # Brand 모델의 stock_qty 필드 값의 합계를 계산
        b_stock = Brand.objects.aggregate(total_stock=Sum("stock_qty"))["total_stock"]

        # 감소된 브랜드의 재고량 및 남은 매출 초기화
        reduced_stock_qty = 0
        min_brand_price = min(brand.price for brand in brand_list)  # 브랜드 상품 최저가

        buy_total = login_user.p_amount // 20000  # 로그인 유저 구매 수량
        print("로그인 유저 총 구매 수량: ", buy_total)
        print("현재 총매출: ", total_sales)
        # 남은 매출 계산
        remain_sales = max(total_sales, 0)

        common_context = {
            "general_all": general_all,
            "general_list": general_list,
            "brand_all": brand_all,
            "brand_list": brand_list,
            "user_list": user_list,
            "g_stock": g_stock,
            "b_stock": b_stock - reduced_stock_qty,
            "total_sales": total_sales,
            "remain_sales": remain_sales,
            "min_brand_price": min_brand_price,
            "buy_total": buy_total,
            "win_user": win_user,
            "not_win_user": not_win_user,
        }
    else:
        common_context = {
            "general_all": general_all,
            "brand_all": brand_all,
        }

    return common_context
