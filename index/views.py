from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import paho.mqtt.client as mqtt
import manage_system.gloabl_var as global_var
from manage_system.settings import BASE_DIR
import cv2, sys
import time, operator
import subprocess
from . import models
import json

mqttBroker = "mqtt.eclipseprojects.io"


def index(request):
    if request.session.get('is_login', None) is None:
        return render(request, '404.html')
    return render(request, 'manage.html')


def publishMsg(request):
    if request.method == 'POST':
        control_msg = request.POST.get('publish_msg', None)
        print('control_msg: ', control_msg)
        if control_msg:
            client = mqtt.Client("control_client")
            client.connect(mqttBroker)
            client.publish("control_msg", control_msg)

    # return redirect('/index/')
    return JsonResponse({"msg": "success"})


def get_info(request):
    return JsonResponse({"msg": global_var.get_value("msg")})


def manage_info(request):
    if request.method == 'POST':
        firm_name = request.POST.get("firm_name")
        license_plate = request.POST.get("license_plate")
        driver_name = request.POST.get("driver_name")
        driver_gender = request.POST.get("driver_gender")
        idcard_number = request.POST.get("idcard_number")
        phone_number = request.POST.get("phone_number")
        pre_deposit_amount = request.POST.get("pre_deposit_amount")
        # 如果数据不存在，则创建，firm_name为主键
        user, b = models.UserInfo.objects.get_or_create(firm_name=firm_name, license_plate=license_plate,
                                                        driver_name=driver_name,
                                                        driver_gender=driver_gender, idcard_number=idcard_number,
                                                        phone_number=phone_number,
                                                        pre_deposit_amount=pre_deposit_amount)
        print(user, b)
        return JsonResponse({"msg": "success"})
    return JsonResponse({"msg": "fail"})


def getImage(request, path):
    if path != '':
        file = open(path, 'rb')
        image_data = file.read()
        file.close()
        return HttpResponse(image_data, content_type="image/png")
    return JsonResponse({"code": 404, "msg": "failed"})


def snapImage(request):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    date1 = time.time()
    src = 'media/' + str(date1) + '.jpg'
    res = cv2.imwrite(src, frame)
    print("snap...")
    cap.release()
    if operator.eq(sys.platform, "linux"):
        cmd = "./myNcnnNet " + str(BASE_DIR) + '/' + src
        print(cmd)
        res = subprocess.getoutput(cmd)
        print(res)
        print("res=", res[0])
        return JsonResponse({"code": 200, "msg": "success", "label": res[0], "src": src})
    else:
        print("非linux尚未实现检测!")
        return JsonResponse({"code": 200, "msg": "success", "src": src})

