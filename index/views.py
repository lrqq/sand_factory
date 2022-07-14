from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import paho.mqtt.client as mqtt
import manage_system.gloabl_var as global_var


mqttBroker = "mqtt.eclipseprojects.io"


def index(request):
    # if request.session.get('is_login', None) is None:
    #     return HttpResponse("尚未登录")
    return render(request, 'index.html')


def publishMsg(request):
    if request.method == 'POST':
        control_msg = request.POST.get('publish_msg', None)
        print('control_msg: ', control_msg)
        if control_msg:
            client = mqtt.Client("Temperature_Inside")
            client.connect(mqttBroker)
            client.publish("control_msg", control_msg)

    # return redirect('/index/')
    return JsonResponse({"msg": "success"})


def get_info(request):
    return JsonResponse({"msg": global_var.get_value("msg")})
