from django.db import models
from patients.models import Patient
from devices.models import Device



#but : stocker les données collectées par les capteurs(valeurs vitales)
class Mesure(models.Model):
    Patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='mesures')
    device= models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    type_donne = models.CharField(max_length=50) #temperature, heart_rate, etc
    valeur = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mesure"