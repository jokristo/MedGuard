from django.db import models
from patients.models import Patient
from devices.models import Device


#but :generer une alerte si une valeur est hors norme
class Alert(models.Model):
    Patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='alerts')
    device= models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    type_alerte = models.CharField(max_length=60) #ex: temperature élevée
    valeur = models.FloatField()
    niveau = models.CharField(max_length=20, choices = [("warning", "Avertissement"),("danger", "Danger")])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Alert"