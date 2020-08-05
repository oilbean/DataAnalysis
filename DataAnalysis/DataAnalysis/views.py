from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse


def home(request):
    return render(request,"home.html")

def count(request):
    return render(request,"count.html")

def serch(request):
    if request.method == 'post':
        pass
    pass
