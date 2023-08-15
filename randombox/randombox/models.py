from django.db import models

# General 과 Brand 모델 둘 다 필드가 동일하므로 Product 하나 만들어서 확장
class Product(models.Model):
    pname = models.CharField(max_length=100, verbose_name="상품명")
    price = models.IntegerField(verbose_name="가격")
    stock_qty = models.IntegerField(verbose_name="재고수량")

    class Meta:
        abstract = True


class General(Product):
    pass


class Brand(Product):
    pass


# 남은 매출만 담는 모델 생성(관리자 페이지에서 데이터 쉽게 가져오려고 만듦)
class Sales(models.Model):
    remain_sales = models.IntegerField(default=0, verbose_name="남은 매출")

    def __str__(self):
        return f"Sales: {self.remain_sales}"
