from django.shortcuts import render

def home(request):
    return render(request,'home.html')

def count(request):
    return render(request,'/base/count.html')