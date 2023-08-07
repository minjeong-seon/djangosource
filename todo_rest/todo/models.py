from django.db import models


class Todo(models.Model):
    """
    필요 칼럼: 제목, 설명, 작성날짜, 완료여부, 중요여부
    """

    title = models.CharField(max_length=50)
    description = models.TextField()
    # DateTimeField 옵션
    # auto_now : 수정할 때마다 날짜/시간이 업데이트 됨
    # auto_now_add : 첫 입력 시 날짜/시간으로 설정됨
    created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
