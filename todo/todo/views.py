from django.shortcuts import render, get_object_or_404, redirect
from .models import Todo
from .forms import TodoForm


# 전체 목록 불러오기
def todo_list(request):
    # 전체 목록 가져오기
    # todos = Todo.objects.all()

    # 미완료된 목록 가져오기
    todos = Todo.objects.filter(complete=False)
    # templates/todo/todo_list.html -- templates 폴더는 자동으로 인식됨(생략가능 -스프링에서 static 같은..)
    return render(request, "todo/todo_list.html", {"todos": todos})


# 리스트 상세 보기
def todo_detail(request, id):
    # id와 일치하는 todo 찾아서 보내기
    todo = get_object_or_404(Todo, id=id)
    return render(request, "todo/todo_detail.html", {"todo": todo})


# 리스트 삽입: insert
def todo_create(request):
    """
    get / post 둘 다 동작하도록 나눠서 작성
    """
    if request.method == "POST":
        # POST로 넘어오는 입력값을 form 객체에 담기
        form = TodoForm(request.POST)
        if form.is_valid():  # 유효성 검증(models.py에 작성한 class field 작성 기준을 따름)
            # important 값은 models.py에서 default=False로 설정했기 때문에 검증 제외
            todo = form.save()  # DB에 insert 작업
            return redirect("todo_detail", id=todo.id)
    else:
        # form이 아닌 get일 때 비어있는 폼 화면에 전송
        form = TodoForm()

    return render(request, "todo/todo_create.html", {"form": form})


# 리스트 수정: update
def todo_edit(request, id):
    # id와 일치하는 todo 찾기
    todo = get_object_or_404(Todo, id=id)
    if request.method == "POST":
        # post : 바인딩 된 form에 post 요청으로 넘어오는 값 담기
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            todo = form.save()
            return redirect("todo_detail", id=todo.id)
    else:
        # get : 찾은 todo를 form에 연결(바인딩)해서 form 전송
        form = TodoForm(instance=todo)

    return render(request, "todo/todo_edit.html", {"form": form, "todo": todo})


# 리스트 삭제: delete
def todo_delete(request, id):
    todo = get_object_or_404(Todo, id=id)
    todo.delete()

    return redirect("todo_list")


# 완료 버튼 클릭 시, 해당 리스트 완료 리스트로 이동: update(set complete = 1)
def todo_done(request, id):
    # 완료할 리스트 todo 찾기
    # 방법1 todo = get_object_or_404(Todo, id=id)
    # 방법2 Objects로 찾기
    todo = Todo.objects.get(id=id)
    # 수정할 todo 값(compplete) 변경
    todo.complete = True
    todo.save()
    return redirect("todo_list")


# 완료 리스트 전체 확인
def done_list(request):
    dones = Todo.objects.filter(complete=True)

    return render(request, "todo/done_list.html", {"dones": dones})
