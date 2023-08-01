from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse


def post_list(request):
    posts = Post.objects.order_by("regdate")
    return render(request, "blogs/post_list.html", {"posts": posts})


@login_required(login_url="users:login")
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)  # request.FILES 추가
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("blog:post_list")
    else:
        form = PostForm()
    return render(request, "blogs/post_write.html", {"form": form})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # 좋아요 여부
    is_liked = False
    # 로그인 사용자가 해당 게시글에 좋아요를 표시했다면
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    context = {"post": post, "is_liked": is_liked}
    return render(request, "blogs/post_detail.html", context)


@login_required(login_url="users:login")
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.updatedate = timezone.now()
            post.save()
            return redirect("blog:post_detail", post_id=post_id)
    else:
        form = PostForm(instance=post)

    return render(request, "blogs/post_edit.html", {"form": form})


@login_required(login_url="users:login")
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect("blog:post_list")


# 좋아요
@login_required(login_url="users:login")
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # 로그인 사용자가 좋아요를 한 게시글인지 확인
    is_liked = post.likes.filter(id=request.user.id).exists()

    is_like_change = False
    if is_liked:
        # 좋아요를 누른 게시글이면 좋아요 정보 삭제
        post.likes.remove(request.user)
    else:
        # 좋아요 추가
        post.likes.add(request.user)
        is_like_change = True
    return JsonResponse({"likes": post.likes.count(), "is_liked": is_like_change})
