from django import template

# from django.utils.safestring import mark_safe

# django 템플릿 등록
# default_if_none|'' : 내용이 없는 경우 공백 처리
# add

# 일련번호 = 전체 게시물 개수 - 시작인덱스 - 현재인덱스 + 1
# 전체 게시물 개수 : 12 (10개씩, 최근 등록순=역순으로 정렬)
# 1 페이지 : 12번째 게시물 ~ 3번째 게시물 (== 12-1-(0~9 인덱스)+1)
# 2 페이지 : 2번째 게시물 ~ 1번째 게시물

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg
