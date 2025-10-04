from rest_framework import serializers
from .models import Mesure
from alerts.views import generer_alerte
from alerts.models import Alert

class MesureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesure
        fields = '__all__'
    
    def create(self, validated_data):
        # Créer la mesure
        mesure = super().create(validated_data)
        
        # Générer l'alerte si nécessaire
        alerte_data = generer_alerte(mesure.type_donne, mesure.valeur)
        
        if alerte_data:
            Alert.objects.create(
                Patient=mesure.Patient,
                device=mesure.device,
                type_alerte=alerte_data['type_alerte'],
                valeur=mesure.valeur,
                niveau=alerte_data['niveau'],
                message=alerte_data['message']
            )
        
        return mesure
