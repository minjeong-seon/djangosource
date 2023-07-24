from django.db import models

"""
photo 앱에서 사용할 테이블 정의
class 로 정의함 - ORM 개념(: 클래스 == 테이블)
"""


class Photo(models.Model):
    """
    create table photo(
        title varchar2(50) not null,
        ...
    ) 와 동일한 과정임

    **models에 정의된 함수로 데이터 타입 설정**
    -문자열 : CharField(max_lengthv=필수임) / TextField()
    -정수 : IntegerField()
    -pk에 해당하는 칼럼은 자동으로 생성됨
    -not null 칼럼으로 생성됨(디폴트) --> null=True 사용해서 nullable 상태로 바꿀 수 있음
    """

    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    image = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
