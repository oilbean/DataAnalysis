from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from DataAnalysis.models import SignEvent


def home(request):
    return render(request,"home.html")

# def count(request):
#     return render(request,"count.html")

def test(request):
    return render(request,"test.html")


def count(request):
    events=SignEvent.objects.all()
    print(events)

    return render(request,"count.html",{"events":events})
