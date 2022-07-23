from django.db import models


class UserInfo(models.Model):
    firm_name = models.CharField(max_length=30, default='大白小黑机器人', primary_key=True)
    license_plate = models.CharField(max_length=30, default='桂A6666', blank=True)
    driver_name = models.CharField(max_length=10, default='张三', blank=True)
    driver_gender = models.CharField(max_length=2, default='', blank=True)
    idcard_number = models.CharField(max_length=30, default='', blank=True)
    phone_number = models.CharField(max_length=30, default='', blank=True)
    pre_deposit_amount = models.IntegerField(default=0, blank=True)

