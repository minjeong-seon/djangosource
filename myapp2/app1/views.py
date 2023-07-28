from django.shortcuts import render


def detail(request):
    return render(request, "app1/detail.html")


def info(request):
    return render(request, "app1/info.html")
