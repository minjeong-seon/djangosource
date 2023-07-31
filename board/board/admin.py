from django.contrib import admin
from .models import Question, Answer, Comment

# Register your models here.


# admin 페이지 question 모델 객체 커스터마이징
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("subject", "regdate")
    search_fields = ["subject"]


# register(상속받은 클래스, <-를 관리할 admin(커스텀)클래스)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Comment)
