from rest_framework import viewsets
from .models import Alert
from .serializers import AlertSerializer


def generer_alerte(type_mesure, valeur):
    if type_mesure == "temperature":
        if valeur > 38:
            return {"type_alerte": "Température élevée", "niveau": "danger", "message": f"Température mesurée à {valeur}°C, supérieure à la normale."}
        elif valeur < 35:
            return {"type_alerte": "Hypothermie", "niveau": "danger", "message": f"Température mesurée à {valeur}°C, inférieure à la normale."}
    elif type_mesure == "blood_pressure":
        if valeur > 140:
            return {"type_alerte": "Hypertension", "niveau": "warning", "message": f"Pression systolique à {valeur} mmHg, supérieure à la normale."}
        elif valeur < 90:
            return {"type_alerte": "Hypotension", "niveau": "warning", "message": f"Pression systolique à {valeur} mmHg, inférieure à la normale."}
    elif type_mesure == "pression_diastolique":
        if valeur > 90:
            return {"type_alerte": "Hypertension diastolique", "niveau": "warning", "message": f"Pression diastolique à {valeur} mmHg, supérieure à la normale."}
        elif valeur < 60:
            return {"type_alerte": "Hypotension diastolique", "niveau": "warning", "message": f"Pression diastolique à {valeur} mmHg, inférieure à la normale."}
    elif type_mesure == "heart_rate":
        if valeur > 100:
            return {"type_alerte": "Tachycardie", "niveau": "warning", "message": f"Fréquence cardiaque à {valeur} bpm, supérieure à la normale."}
        elif valeur < 60:
            return {"type_alerte": "Bradycardie", "niveau": "warning", "message": f"Fréquence cardiaque à {valeur} bpm, inférieure à la normale."}
    elif type_mesure == "saturation_o2":
        if valeur < 95:
            return {"type_alerte": "Hypoxémie", "niveau": "danger", "message": f"Saturation O₂ à {valeur}%, inférieure à la normale."}
    elif type_mesure == "glucose":
        if valeur > 126:  # Correction du seuil (126 g/L au lieu de 1.26)
            return {"type_alerte": "Hyperglycémie", "niveau": "danger", "message": f"Glycémie à {valeur} g/L, supérieure à la normale."}
    elif valeur < 70:  # Correction du seuil (70 g/L au lieu de 0.7)
        return {"type_alerte": "Hypoglycémie", "niveau": "danger", "message": f"Glycémie à {valeur} g/L, inférieure à la normale."}
    return None



class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
