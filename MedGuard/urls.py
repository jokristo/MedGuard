"""
URL configuration for MedGuard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from MedGuard.views import home_view
from rest_framework import routers
from patients.views import PatientViewSet
from devices.views import DeviceViewSet
from mesures.views import MesureViewSet
from alerts.views import AlertViewSet
from ai_module.predictor import PredictRisk
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuration du routeur pour les ViewSets
router = routers.DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'devices', DeviceViewSet)
router.register(r'mesures', MesureViewSet)
router.register(r'alerts', AlertViewSet)

# Configuration de la documentation Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="MedGuard API",
        default_version='v1',
        description="API pour le système de surveillance médicale MedGuard",
        contact=openapi.Contact(email="support@medguard.com"),
    ),
    public=True,
)

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/predict-risk/', PredictRisk.as_view(), name='predict-risk'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
