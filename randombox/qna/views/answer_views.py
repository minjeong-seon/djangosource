from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from ..models import Question, Answer
from users.models import CustomUser
from ..forms import AnswerForm
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@login_required(login_url="users:login")
def answer_create(request, qid):
    question = get_object_or_404(Question, id=qid)
    question_author = CustomUser.objects.get(username=question.author.username)

    if request.method == "POST":
        form = AnswerForm(request.POST)

        if form.is_valid():
            answer = form.save(commit=False)

            answer.question = question
            answer.author = request.user
            answer.save()

            # 이메일 발송
            reply_email = EmailMessage(
                "답변 등록 안내",
                f"안녕하세요. {question_author.username} 님,\n\n등록하신 질문에 대한 답변이 등록되었습니다. \n\n질문 제목: {question.title}\n\n답변 확인하기: http://127.0.0.1:8000/qna/{question.id}/",
                to=[question_author.email],
            )

            reply_email.send()

            return redirect(
                "{}#answer_{}".format(resolve_url("qna:detail", qid=qid), answer.id)
            )

    else:
        form = AnswerForm()

    context = {"question": question, "form": form}
    return render(request, "qna/question_detail.html", context)


@login_required(login_url="users:login")
def answer_edit(request, aid, qid):
    answer = get_object_or_404(Answer, id=aid)
    question = get_object_or_404(Question, id=qid)
    question_author = CustomUser.objects.get(username=question.author.username)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.updatedate = timezone.now()
            answer.save()

            # 이메일 발송
            reply_email = EmailMessage(
                "답변 재등록 안내",
                f"안녕하세요. {question_author.username} 님,\n\n등록하신 질문에 대한 답변이 재등록되었습니다. \n\n질문 제목: {question.title}\n\n답변 확인하기: http://127.0.0.1:8000/qna/{question.id}/",
                to=[question_author.email],
            )

            reply_email.send()

            return redirect("qna:detail", qid=qid)
    else:
        form = AnswerForm(instance=answer)
    return render(
        request,
        "qna/answer_edit.html",
        {"question": question, "form": form, "answer": answer},
    )


def answer_delete(request, aid):
    answer = get_object_or_404(Answer, id=aid)
    answer.delete()

    return redirect("qna:detail", qid=answer.question.id)
