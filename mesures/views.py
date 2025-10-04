from rest_framework import viewsets
from .models import Mesure
from .serializers import MesureSerializer
from alerts.views import generer_alerte
from alerts.models import Alert
from rest_framework.response import Response
from rest_framework import status

class MesureViewSet(viewsets.ModelViewSet):
    queryset = Mesure.objects.all()
    serializer_class = MesureSerializer

    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        
        # Sauvegarder les mesures
        mesures = serializer.save()
        
        # Générer les alertes pour chaque mesure
        if is_many:
            for mesure in mesures:
                self._generer_alertes_pour_mesure(mesure)
        else:
            self._generer_alertes_pour_mesure(mesures)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def _generer_alertes_pour_mesure(self, mesure):
        """Génère une alerte si la valeur de la mesure est hors norme"""
        alerte_data = generer_alerte(mesure.type_donne, mesure.valeur)
        
        if alerte_data:
            # Créer l'alerte dans la base de données
            Alert.objects.create(
                Patient=mesure.Patient,
                device=mesure.device,
                type_alerte=alerte_data['type_alerte'],
                valeur=mesure.valeur,
                niveau=alerte_data['niveau'],
                message=alerte_data['message']
            )
