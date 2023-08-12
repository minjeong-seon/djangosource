# 주소 필드 추가하고 싶을 때 AbstractUser 상속받아서 커스텀 유저 생성 후 address 필드 추가하기
from django.contrib.auth.models import AbstractUser
from django.db import models
from randombox.models import General, Brand


class CustomUser(AbstractUser):
    # 주소 필드 추가
    address = models.CharField(max_length=255)
    # 구매금액 필드 추가
    p_amount = models.IntegerField()
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, null=True, blank=True  # Product 모델 사용
    )

    # CustomUser 모델의 general 필드(Attribute 생성x)에 General 모델의 데이터가 List 구조로 삽입됨
    general = models.ManyToManyField(General, related_name="custom_users", blank=True)

    def __str__(self):
        return self.username
