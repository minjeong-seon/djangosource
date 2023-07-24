from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Photo
from .forms import PhotoForm

"""
render(request객체, 템플릿이름)

-템플릿을 저장하는 폴더 기본값 : 앱 > templates
"""


# photo 테이블에 저장된 디비 정보 전체 불러오기 : photo list
def photo_list(request):
    # 단순하게 문자열만 화면에 표시할 때
    # return HttpResponse("Hello Photo!")

    # 템플릿 페이지 화면에 보여주기
    # return render(request, "photo_list.html")

    # 템플릿 + DB 데이터 보여주기(=딕셔너리 형태{"key":value}필요)
    photos = Photo.objects.all()  # photo 테이블 가져오기 == select * from photo
    return render(request, "photo_list.html", {"photos": photos})


# photo 테이블 내 데이터 하나 불러오기 : photo read one
def photo_detail(request, id):
    # get_object_or_404(Photo, id=id) : id를 이용해서 불러올 데이터가 있으면 Photo 객체에 담고, 없으면 404 반환
    photo = get_object_or_404(Photo, id=id)
    return render(request, "photo_detail.html", {"photo": photo})


# **모델폼을 사용하지 않는 방식**
# # photo 테이블 지정 데이터 삽입 : insert
# def photo_add(request):
#     """
#     request 객체의 method 방식에 다라서 처리 방법을 다르게 작성함

#     """
#     if request.method == "POST":
#         title = request.POST["title"]
#         author = request.POST["author"]
#         image = request.POST["image"]
#         description = request.POST["description"]
#         price = request.POST["price"]
#         # print(title, author, image, description, price)

#         # DB 작업 : 삽입할 객체 생성
#         photo = Photo(
#             title=title,
#             author=author,
#             image=image,
#             description=description,
#             price=price,
#         )
#         # 생성된 객체 저장(== DB에 insert 작업 실행)
#         photo.save()

#         # 잘 저장됐는지 photo_list.html로 이동
#         # return redirect("/photo/")
#         return redirect("photo_list")

#     return render(request, "photo_post.html")


# photo_add 함수 : 모델폼을 사용하는 방식
def photo_add(request):
    """
    request 객체의 method 방식에 다라서 처리 방법을 다르게 작성함

    """
    if request.method == "POST":
        form = PhotoForm(request.POST)
        if form.is_valid():
            form.save()  # form은 model과 연결된 상황이므로 바로 insert 작업 이루어짐
            return redirect("photo_list")
    else:
        form = PhotoForm()

    return render(request, "photo_post.html", {"form": form})


# **모델폼을 사용하지 않는 방식**
# Photo 테이블 데이터 수정 : update 작업
# def photo_edit(request, id):
#     photo = get_object_or_404(Photo, id=id)

#     if request.method == "POST":
#         title = request.POST["title"]
#         price = request.POST["price"]

#         photo.title = title
#         photo.price = price
#         photo.save()  # update / insert 둘 다 가능함
#         # 상세보기 이동 /photo/1
#         # return redirect("/photo/{}/".format(id))
#         return redirect("photo_detail", id=photo.id)

#     return render(request, "photo_edit.html", {"photo": photo})


# photo_edit 함수 : 모델폼을 사용하는 방식
def photo_edit(request, id):
    photo = get_object_or_404(Photo, id=id)

    if request.method == "POST":
        # POST로 넘어오는 수정값도 PhotoForm에 담겨져 있는 상황
        form = PhotoForm(request.POST, instance=photo)
        if form.is_valid():  # table 생성 규칙에 맞는지 검증(데이터 타입, 제약조건 등 model.py에 정의한 규칙)
            form.save()
            return redirect("photo_detail", id=photo.id)
    else:
        # 위에서 찾은 db 데이터를 form에 담아서 보내기
        form = PhotoForm(instance=photo)

    return render(request, "photo_edit.html", {"form": form})


def photo_delete(request, id):
    """
    삭제 후 목록보기로 이동 : delete + page move
    """

    # 삭제할 대상 찾기(id 값을 이용하기)
    photo = get_object_or_404(Photo, id=id)
    photo.delete()  # delete from~~ 쿼리문이랑 같은 역할

    return redirect("photo_list")
