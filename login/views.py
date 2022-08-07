import json

from django.shortcuts import render, redirect
from django.http import HttpResponse


# Create your views here.
def login(request):
    ret = {"flag": False, "error_msg": None}
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        print(request.POST)
        userName = request.POST.getlist('user')[0]
        password = request.POST.getlist('pwd')[0]
        print(userName, password, type(userName))
        if userName == 'admin' and password == '2022':
            # request.session可以做到带参数跳转页面
            request.session['is_login'] = True
            ret["flag"] = True
            return HttpResponse(json.dumps(ret))
        else:
            ret["error_msg"] = "登录失败"
            return HttpResponse(json.dumps(ret))


def detail(request):
    return render(request, 'detail.html')
