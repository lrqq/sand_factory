from django.shortcuts import render, redirect
from django.http import HttpResponse


# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        print(request.POST)
        userName = request.POST.get('user')
        password = request.POST.get('pwd')
        if userName == 'gxu' and password == '2022':
            request.session['is_login'] = True
            return redirect('/index/')
        else:
            return render(request, 'login.html', {"error_msg": "登录失败，用户名或密码错误。"})


def detail(request):
    return render(request, 'detail.html')
