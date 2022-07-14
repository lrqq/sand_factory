from django.db import models


class Temperature_Humidity(models.Model):
    temperature = models.CharField(max_length=10)
    humidity = models.CharField(max_length=10)
    
