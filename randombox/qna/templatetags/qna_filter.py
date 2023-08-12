from django import template

# QNA 게시판 페이지 나누기를 위한 필터

register = template.Library()

# @register.filter : 템플릿에 적용할 커스텀 필터 정의하려는 함수에 붙이는 데코레이터
# value, arg : value = 필터 적용할 값, arg = 필터에 전달되는 추가 인자
# value - arg : value에서 arg를 차감한 값을 템플릿에 리턴

# 한 번에 보여지는 페이지 수가 최대 10이면 arg = 5면 총 5페이지만 보여줌.
# 템플릿에서 사용 시 상단에 import 구문 : {% load qna_filter %}


@register.filter
def sub(value, arg):
    return value - arg


@register.filter(name="modify_author")
def modify_author(author):
    return author.username[:-2] + "**"
