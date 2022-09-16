import random
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
    res = {}
    # 如果检测到地磅信号，则进行检测
    if global_var.get_value("status") == "weight_ok":
        global_var.set_value("status", "not")
        src = snap_detect()
        if src:
            res["src"] = src
        if global_var.get_value("detect_status") == "ok":
            global_var.set_value("detect_status", "not")
            client = mqtt.Client(client_id=f'client-{random.randint(0, 1000)}', clean_session=False)
            client.connect(mqttBroker)
            client.publish("control_msg", "3")
            time.sleep(1)
            client.publish("control_msg", "1")
        res["state"] = "ok"
        res["car_id"] = global_var.get_value("car_id")
        res["sand_type"] = global_var.get_value("sand_type")
        res["total_weight"] = global_var.get_value("total_weight")
        return JsonResponse(res)
    else:
        return JsonResponse(
            {"src": "null", "state": "not", "car_id": "null", "sand_type": "null", "total_weight": "null"})


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


# 客户端的浏览器请求了才能执行
def snapImage(request):
    cap = cv2.VideoCapture(0)
    for i in range(5):
        time.sleep(0.01)
        ret, frame = cap.read()
    if ret:
        print("snapping...")
    else:
        print("can't snap, check index/views.py/snap_detect()")
        return JsonResponse({"code": 200, "msg": "success", "src": './'})
    date1 = time.time()
    src = 'media/' + str(date1) + '.jpg'
    res = cv2.imwrite(src, frame)
    print("snap...")
    print(res)
    cap.release()
    if operator.eq(sys.platform, "linux"):
        cmd = "./myNcnnNet " + str(BASE_DIR) + '/' + src
        print(cmd)
        res = subprocess.getoutput(cmd)
        print(res)
        print("res=", res[0])
        global_var.set_value("sand_type", res[0])
        return JsonResponse({"code": 200, "msg": "success", "label": res[0], "src": src})
    else:
        print("非linux尚未实现检测!")
        return JsonResponse({"code": 200, "msg": "success", "src": src})


# 直接进行拍照和检测
def snap_detect():
    print("prepare to snap...")
    cap = cv2.VideoCapture(0)
    for i in range(5):
        time.sleep(0.01)
        ret, frame = cap.read()
    if ret:
        print("snapping...")
    else:
        print("can't snap, check index/views.py/snap_detect()")
        return False
    date1 = time.time()
    src = 'media/' + str(date1) + '.jpg'
    res = cv2.imwrite(src, frame)
    if res:
        print("snap done.")
    cap.release()
    if operator.eq(sys.platform, "linux"):
        cmd = "./myNcnnNet " + str(BASE_DIR) + '/' + src
        print(cmd)
        res = subprocess.getoutput(cmd)
        print(res)
        print("res=", res[0])
        global_var.set_value("sand_type", res[0])
        global_var.set_value("detect_status", "ok")
        return src
    else:
        print("非linux尚未实现检测!")
        global_var.set_value("sand_type", 0)
        global_var.set_value("detect_status", "ok")
        # global_var.set_value("detect_status", "not")
        return src
        # return False
