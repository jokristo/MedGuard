from django.db import models


#but : gerer les utilisateurs/patients et leurs infos medicales de base
class Patient(models.Model):
    nom = models.CharField(max_length=100)
    age = models.IntegerField()
    sexe = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Patient"
