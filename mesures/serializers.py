from rest_framework import serializers
from .models import Mesure

class MesureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesure
        fields = '__all__'
        