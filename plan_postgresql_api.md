# Plan d'Implémentation PostgreSQL et API MedGuard

## 1. Configuration PostgreSQL avec Docker

### Fichier docker-compose.yml
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: medguard_db
      POSTGRES_USER: medguard_user
      POSTGRES_PASSWORD: medguard
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U medguard_user -d medguard_db"]
      interval: 30s
      timeout: 10s
      retries: 5

volumes:
  postgres_data:
```

### Configuration Django (settings.py)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'medguard_db',
        'USER': 'medguard_user',
        'PASSWORD': 'medguard',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 2. Installation des Dépendances Nécessaires

Ajouter à requirements.txt:
```
psycopg2-binary==2.9.9
django-cors-headers==4.3.1
drf-yasg==1.21.7
```

## 3. Sérialiseurs Django REST Framework

### patients/serializers.py
```python
from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
```

### devices/serializers.py
```python
from rest_framework import serializers
from .models import Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
```

### mesures/serializers.py
```python
from rest_framework import serializers
from .models import Mesure

class MesureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesure
        fields = '__all__'
```

### alerts/serializers.py
```python
from rest_framework import serializers
from .models import Alert

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'
```

## 4. Endpoints CRUD

### patients/views.py
```python
from rest_framework import viewsets
from .models import Patient
from .serializers import PatientSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
```

### devices/views.py
```python
from rest_framework import viewsets
from .models import Device
from .serializers import DeviceSerializer

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
```

### mesures/views.py
```python
from rest_framework import viewsets
from .models import Mesure
from .serializers import MesureSerializer

class MesureViewSet(viewsets.ModelViewSet):
    queryset = Mesure.objects.all()
    serializer_class = MesureSerializer
```

### alerts/views.py
```python
from rest_framework import viewsets
from .models import Alert
from .serializers import AlertSerializer

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
```

## 5. Configuration des URLs

### MedGuard/urls.py
```python
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from patients.views import PatientViewSet
from devices.views import DeviceViewSet
from mesures.views import MesureViewSet
from alerts.views import AlertViewSet
from ai_module.predictor import PredictRisk

router = routers.DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'devices', DeviceViewSet)
router.register(r'mesures', MesureViewSet)
router.register(r'alerts', AlertViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/predict-risk/', PredictRisk.as_view(), name='predict-risk'),
    path('api-auth/', include('rest_framework.urls')),
]
```

## 6. Documentation API avec Swagger

Ajouter dans settings.py:
```python
INSTALLED_APPS = [
    # ... autres apps
    'drf_yasg',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ... autres middleware
]

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}
```

Ajouter dans urls.py:
```python
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="MedGuard API",
        default_version='v1',
        description="API pour le système de surveillance médicale MedGuard",
    ),
    public=True,
)

urlpatterns = [
    # ... autres URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```

## 7. Étapes d'Exécution

1. `docker-compose up -d` pour lancer PostgreSQL
2. `pip install -r requirements.txt` pour installer les dépendances
3. `python manage.py makemigrations`
4. `python manage.py migrate`
5. `python manage.py runserver`

## 8. Tests des Endpoints

Endpoints disponibles:
- `GET/POST/PUT/DELETE /api/patients/`
- `GET/POST/PUT/DELETE /api/devices/`
- `GET/POST/PUT/DELETE /api/mesures/`
- `GET/POST/PUT/DELETE /api/alerts/`
- `POST /api/predict-risk/`
- `GET /swagger/` pour la documentation