from rest_framework.views import APIView
from rest_framework.response import Response


class PredictRisk(APIView):
    def post(self, request):
        data = request.data
        #Exemple : on recupere temperature, bpm, glycemie
        temp = data.get("temperature")
        bpm = data.get("heart_rate")
        glucose = data.get("glucose")

        #simuler une prédiction(à remplacer par un vrai modele ML )
        risk = "élevé" if glucose > 150 or temp > 38 else "faible"

        return Response({"risque_diabete":risk})