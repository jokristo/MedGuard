from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Avg, Max, Min
from django.utils import timezone
from datetime import timedelta
from .models import Mesure

@admin.register(Mesure)
class MesureAdmin(admin.ModelAdmin):
    # Configuration de la liste
    list_display = ['type_donne', 'valeur', 'patient_link', 'device_link', 'timestamp', 'is_critical']
    list_filter = ['type_donne', 'timestamp', 'Patient__sexe']
    search_fields = ['type_donne', 'Patient__nom', 'device__device_id']
    ordering = ['-timestamp']
    date_hierarchy = 'timestamp'
    list_per_page = 50
    
    # Configuration du formulaire d'édition
    fieldsets = (
        ('Données de Mesure', {
            'fields': ('type_donne', 'valeur', 'timestamp')
        }),
        ('Sources', {
            'fields': ('Patient', 'device')
        }),
    )
    readonly_fields = ['timestamp']
    
    # Fonctions personnalisées pour les liens et indicateurs
    def patient_link(self, obj):
        if obj.Patient:
            url = reverse('admin:patients_patient_change', args=[obj.Patient.id])
            return format_html('<a href="{}">{}</a>', url, obj.Patient.nom)
        return "Aucun patient"
    patient_link.short_description = 'Patient'
    
    def device_link(self, obj):
        if obj.device:
            url = reverse('admin:devices_device_change', args=[obj.device.id])
            return format_html('<a href="{}">{}</a>', url, obj.device.device_id)
        return "Aucun device"
    device_link.short_description = 'Device'
    
    def is_critical(self, obj):
        # Déterminer si la valeur est critique selon le type de donnée
        critical_ranges = {
            'temperature': (35.0, 38.5),
            'heart_rate': (60, 100),
            'blood_pressure_systolic': (90, 140),
            'blood_pressure_diastolic': (60, 90),
            'oxygen_saturation': (95, 100),
        }
        
        if obj.type_donne in critical_ranges:
            min_val, max_val = critical_ranges[obj.type_donne]
            if obj.valeur < min_val or obj.valeur > max_val:
                return format_html('<span style="color: red; font-weight: bold;">CRITIQUE</span>')
        
        return format_html('<span style="color: green;">Normal</span>')
    is_critical.short_description = 'Statut'
    
    # Actions personnalisées
    actions = ['export_measures_data', 'analyze_trends']
    
    def export_measures_data(self, request, queryset):
        self.message_user(request, f"Données de {queryset.count()} mesure(s) préparées pour l'export.")
    export_measures_data.short_description = "Exporter les données de mesures"
    
    def analyze_trends(self, request, queryset):
        self.message_user(request, f"Analyse des tendances pour {queryset.count()} mesure(s) lancée.")
    analyze_trends.short_description = "Analyser les tendances"
    
    # Filtres personnalisés
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Filtrer les mesures critiques si demandé
        if request.GET.get('critical_only') == 'true':
            critical_ranges = {
                'temperature': (35.0, 38.5),
                'heart_rate': (60, 100),
                'blood_pressure_systolic': (90, 140),
                'blood_pressure_diastolic': (60, 90),
                'oxygen_saturation': (95, 100),
            }
            
            from django.db.models import Q
            conditions = Q()
            for measure_type, (min_val, max_val) in critical_ranges.items():
                conditions |= Q(type_donne=measure_type, valeur__lt=min_val)
                conditions |= Q(type_donne=measure_type, valeur__gt=max_val)
            
            qs = qs.filter(conditions)
        
        return qs
    
    # Panneau de statistiques personnalisé
    def changelist_view(self, request, extra_context=None):
        # Statistiques des mesures
        now = timezone.now()
        last_24h = now - timedelta(hours=24)
        
        stats = {
            'total_measures': Mesure.objects.count(),
            'last_24h_measures': Mesure.objects.filter(timestamp__gte=last_24h).count(),
            'by_type': Mesure.objects.values('type_donne').annotate(
                count=Count('id'),
                avg=Avg('valeur'),
                max=Max('valeur'),
                min=Min('valeur')
            ),
            'recent_measures': Mesure.objects.order_by('-timestamp')[:10],
        }
        
        # Calculer les mesures critiques
        critical_ranges = {
            'temperature': (35.0, 38.5),
            'heart_rate': (60, 100),
            'blood_pressure_systolic': (90, 140),
            'blood_pressure_diastolic': (60, 90),
            'oxygen_saturation': (95, 100),
        }
        
        critical_count = 0
        for measure_type, (min_val, max_val) in critical_ranges.items():
            critical_count += Mesure.objects.filter(
                type_donne=measure_type,
                valeur__lt=min_val
            ).count()
            critical_count += Mesure.objects.filter(
                type_donne=measure_type,
                valeur__gt=max_val
            ).count()
        
        stats['critical_measures'] = critical_count
        
        extra_context = extra_context or {}
        extra_context['stats'] = stats
        
        return super().changelist_view(request, extra_context=extra_context)
