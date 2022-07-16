from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import paho.mqtt.client as mqtt
import manage_system.gloabl_var as global_var
import cv2
import time

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

def snapImage(request):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    date1 = time.time()
    src = 'media/' + str(date1) + '.jpg'
    res = cv2.imwrite(src,frame)
    print("snap...")
    cap.release()
    return JsonResponse({"code":200,"msg": "success","src":src})

def getImage(request,path):
    print(path)
    if path!='':
        image_data = open(path,'rb').read()
        return HttpResponse(image_data,content_type = "image/png")
    return JsonResponse({"code":404,"msg": "failed"})
