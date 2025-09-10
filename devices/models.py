from django.db import models
from patients.models import Patient


#but : lier chaque patient à un ESP32/capteur
class Device(models.Model):
    Patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='devices')
    device_id = models.CharField(max_length=100, unique=True)
    type_capteur = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Device"
