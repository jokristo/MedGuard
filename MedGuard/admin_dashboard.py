from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Count, Avg, Max, Min, Q
from django.utils import timezone
from datetime import timedelta
from patients.models import Patient
from devices.models import Device
from mesures.models import Mesure
from alerts.models import Alert

def admin_dashboard(request):
    """Dashboard personnalisé pour l'administration MedGuard"""
    
    # Calculer les statistiques en temps réel
    now = timezone.now()
    last_24h = now - timedelta(hours=24)
    last_7d = now - timedelta(days=7)
    
    # Statistiques des patients
    patient_stats = {
        'total': Patient.objects.count(),
        'avg_age': Patient.objects.aggregate(avg_age=Avg('age'))['avg_age'] or 0,
        'by_sex': Patient.objects.values('sexe').annotate(count=Count('id')),
        'recent': Patient.objects.order_by('-created_at')[:5],
    }
    
    # Statistiques des devices
    device_stats = {
        'total': Device.objects.count(),
        'active': Device.objects.filter(status=True).count(),
        'inactive': Device.objects.filter(status=False).count(),
        'by_type': Device.objects.values('type_capteur').annotate(count=Count('id')),
    }
    
    # Statistiques des mesures
    mesure_stats = {
        'total': Mesure.objects.count(),
        'last_24h': Mesure.objects.filter(timestamp__gte=last_24h).count(),
        'by_type': Mesure.objects.values('type_donne').annotate(
            count=Count('id'),
            avg=Avg('valeur'),
            max=Max('valeur'),
            min=Min('valeur')
        ),
    }
    
    # Statistiques des alertes
    alert_stats = {
        'total': Alert.objects.count(),
        'unresolved': Alert.objects.filter(resolved_at__isnull=True).count(),
        'last_24h': Alert.objects.filter(created_at__gte=last_24h).count(),
        'by_level': Alert.objects.values('niveau').annotate(count=Count('id')),
        'recent_critical': Alert.objects.filter(
            niveau='danger', 
            resolved_at__isnull=True
        ).order_by('-created_at')[:10],
    }
    
    # Calculer les mesures critiques
    critical_ranges = {
        'temperature': (35.0, 38.5),
        'heart_rate': (60, 100),
        'blood_pressure_systolic': (90, 140),
        'blood_pressure_diastolic': (60, 90),
        'oxygen_saturation': (95, 100),
    }
    
    critical_measures = 0
    for measure_type, (min_val, max_val) in critical_ranges.items():
        critical_measures += Mesure.objects.filter(
            type_donne=measure_type,
            valeur__lt=min_val
        ).count()
        critical_measures += Mesure.objects.filter(
            type_donne=measure_type,
            valeur__gt=max_val
        ).count()
    
    mesure_stats['critical'] = critical_measures
    
    # Tendances des 7 derniers jours
    trends = {
        'patients': Patient.objects.filter(created_at__gte=last_7d).count(),
        'devices': Device.objects.filter().count(),  # Tous les devices
        'measures': Mesure.objects.filter(timestamp__gte=last_7d).count(),
        'alerts': Alert.objects.filter(created_at__gte=last_7d).count(),
    }
    
    context = {
        'title': 'Dashboard MedGuard',
        'patient_stats': patient_stats,
        'device_stats': device_stats,
        'mesure_stats': mesure_stats,
        'alert_stats': alert_stats,
        'trends': trends,
        'now': now,
    }
    
    return render(request, 'admin/dashboard.html', context)

# Ajouter la vue au site admin
admin.site.index_template = 'admin/dashboard.html'
admin.site.site_header = 'Administration MedGuard'
admin.site.site_title = 'MedGuard Admin'
admin.site.index_title = 'Tableau de Bord'

# Créer une URL pour le dashboard
def get_admin_urls():
    urls = super(admin.AdminSite, admin.site).get_urls()
    custom_urls = [
        path('dashboard/', admin.site.admin_view(admin_dashboard), name='admin_dashboard'),
    ]
    return custom_urls + urls

admin.site.get_urls = get_admin_urls