from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Todo
from .serializer import TodoSerializer


class TodoApiView(APIView):
    def get(self, request):
        # complete 가 false 인 전체 todo 조회
        todos = Todo.objects.filter(complete=False)
        # 조회된 전체 todo를 TodoSerializer에 담기
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# def tidi_list(request):
#     if request.method == "POST":
#         todos = Todo.objects.filter(complete=False)
#         return render(request, "템플릿 파일명", {todos:todos})
