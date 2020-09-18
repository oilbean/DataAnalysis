from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from DataAnalysis.models import SignEvent


def home(request):
    return render(request,"home.html")

def test(request):
    return render(request,"test.html")

def count(request):
    events=SignEvent.objects.all()

    return render(request,"count.html",{"events":events})

def search(request):
    #获取前端搜索字段
    search_name=request.GET.get("name",'')

    search_add=request.GET.get("address",'')

    #查询数据
    event_list=SignEvent.objects.filter(name__contains=search_name).filter(address__contains=search_add)

    return render(request,"count.html",{"events":event_list})


def edit(request):

    if request.method == 'POST':

        id=request.POST['id']
        name= request.POST['name']
        address=request.POST['address']
        status=request.POST['status']


        SignEvent.objects.filter(id=id).update(name=name,address=address,status=status)

        return HttpResponseRedirect("base/count/")

    id = request.GET["event_id"]

    event = SignEvent.objects.filter(id=id)
    return render(request,"edit.html",{"event":event[0]})

def paginator_view(request):
    pass