from django.db import models


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


class Sales(models.Model):
    remain_sales = models.IntegerField(default=0, verbose_name="남은 매출")
