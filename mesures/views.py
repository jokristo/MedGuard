from rest_framework import viewsets
from .models import Mesure
from .serializers import MesureSerializer

from rest_framework.response import Response
from rest_framework import status

class MesureViewSet(viewsets.ModelViewSet):
    queryset = Mesure.objects.all()
    serializer_class = MesureSerializer

    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)