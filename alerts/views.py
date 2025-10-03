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
        if valeur > 1.26:
            return {"type_alerte": "Hyperglycémie", "niveau": "danger", "message": f"Glycémie à {valeur} g/L, supérieure à la normale."}
        elif valeur < 0.7:
            return {"type_alerte": "Hypoglycémie", "niveau": "danger", "message": f"Glycémie à {valeur} g/L, inférieure à la normale."}
    elif type_mesure == "frequence_respiratoire":
        if valeur > 20:
            return {"type_alerte": "Polypnée", "niveau": "warning", "message": f"Fréquence respiratoire à {valeur} cpm, supérieure à la normale."}
        elif valeur < 12:
            return {"type_alerte": "Bradypnée", "niveau": "warning", "message": f"Fréquence respiratoire à {valeur} cpm, inférieure à la normale."}
    # elif type_mesure == "poids":
    #     if valeur < 40:
    #         return {"type_alerte": "Poids très faible", "niveau": "warning", "message": f"Poids à {valeur} kg, très inférieur à la normale."}
    # elif type_mesure == "taille":
    #     if valeur < 1.3:
    #         return {"type_alerte": "Petite taille", "niveau": "info", "message": f"Taille à {valeur} m, inférieure à la normale."}
    # elif type_mesure == "imc":
    #     if valeur > 30:
    #         return {"type_alerte": "Obésité", "niveau": "warning", "message": f"IMC à {valeur}, supérieur à la normale."}
    #     elif valeur < 18.5:
    #         return {"type_alerte": "Maigreur", "niveau": "warning", "message": f"IMC à {valeur}, inférieur à la normale."}
    # # Ajoute ici d'autres types de mesures selon tes besoins
    return None



class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
