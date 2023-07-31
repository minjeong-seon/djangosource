from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from ..models import Question, Answer, Comment
from ..forms import CommentForm

from django.contrib.auth.decorators import login_required
from django.utils import timezone


################ 질문 댓글 #################
@login_required(login_url="users:login")
def comment_create_q(request, qid):
    """
    질문 댓글 추가 - question id 필요함
    """
    # 질문 찾기
    question = get_object_or_404(Question, id=qid)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(
                commit=False
            )  # form 안에 user, question 정보 아직 안 담겼음(커밋 x)
            comment.author = request.user
            comment.question = question
            comment.save()
            # return redirect("board:detail", qid=qid)
            return redirect(
                "{}#comment_{}".format(resolve_url("board:detail", qid=qid), comment.id)
            )

    else:
        form = CommentForm()

    return render(request, "board/comment_form.html", {"form": form})

    pass


@login_required(login_url="users:login")
def comment_edit_q(request, cid):
    """
    질문 댓글 수정 - comment id 필요
    """
    comment = get_object_or_404(Comment, id=cid)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)  # 댓글 수정날짜 데이터 추가해야 됨
            comment.updatedate = timezone.now()
            comment.save()
            # return redirect("board:detail", qid=comment.question.id)
            return redirect(
                "{}#comment_{}".format(
                    resolve_url("board:detail", qid=comment.answer.question.id),
                    comment.id,
                )
            )

    else:
        form = CommentForm(instance=comment)

    return render(request, "board/comment_form.html", {"form": form})


@login_required(login_url="users:login")
def comment_delete_q(request, cid):
    """
    질문 댓글 삭제 - comment id 필요
    """
    # 댓글 하나 가져오기
    comment = get_object_or_404(Comment, id=cid)

    # 댓글 삭제 -> 삭제 후 detail페이지로 이동
    comment.delete()
    return redirect("board:detail", qid=comment.question.id)


################ 답변 댓글 #################
@login_required(login_url="users:login")
def comment_create_a(request, aid):
    """
    답변 댓글 추가 - answer id 필요
    """
    answer = get_object_or_404(Answer, id=aid)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.answer = answer
            comment.save()
            # return redirect("board:detail", qid=answer.question.id)/
            return redirect(
                "{}#comment_{}".format(
                    resolve_url("board:detail", qid=answer.question.id), comment.id
                )
            )

    else:
        form = CommentForm()
    return render(request, "board/comment_form.html", {"form": form})


@login_required(login_url="users:login")
def comment_edit_a(request, cid):
    comment = get_object_or_404(Comment, id=cid)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.updatedate = timezone.now()
            comment.save()
            # return redirect("board:detail", qid=comment.answer.question.id)
            return redirect(
                "{}#answer_{}".format(
                    resolve_url("board:detail", qid=comment.answer.question.id)
                ),
                comment.id,
            )
    else:
        form = CommentForm(instance=comment)
    return render(request, "board/comment_form.html", {"form": form})


@login_required(login_url="users:login")
def comment_delete_a(request, cid):
    # 댓글 하나 가져오기
    comment = get_object_or_404(Comment, id=cid)

    # 댓글 삭제 -> 삭제 후 detail페이지로 이동
    comment.delete()
    # comment 데이터에는 question.id 정보가 없음(답변에 대한 댓글이라)
    # answer 를 통해 question.id 값을 가져와야 함
    return redirect("board:detail", qid=comment.answer.question.id)
