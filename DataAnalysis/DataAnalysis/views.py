from django.shortcuts import render
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from DataAnalysis.models import SignEvent
from django.db import connection


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



    paginator = Paginator(event_list, 2)

    page = request.GET.get('page')

    try:
        event_list = paginator.page(page)
    except PageNotAnInteger:
        event_list = paginator.page(1)
    except EmptyPage:
        event_list = paginator.page(paginator.num_pages)

    return render(request,"count.html",{"events":event_list,
                                        "name":search_name,
                                        "address":search_add})


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

    event_list = SignEvent.objects.all()
    paginator = Paginator(event_list,2)

    page = request.GET.get('page')

    try:
        events=paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)


    return render(request,'count.html',{'events':events})

def sql(request):
    cursor = connection.cursor()
    cursor.execute("select * from sign_event")
    raw=cursor.fetchall()

    print(raw)
    paginator = Paginator(raw, 2)

    page = request.GET.get('page')

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    print("%%%%%%%%%%")
    print(events)
    return render(request, 'count.html', {'events': events})
