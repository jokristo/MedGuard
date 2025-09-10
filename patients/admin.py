from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Avg
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    # Configuration de la liste
    list_display = ['nom', 'age', 'sexe', 'email', 'created_at', 'devices_count', 'mesures_count', 'alerts_count']
    list_filter = ['sexe', 'created_at', 'age']
    search_fields = ['nom', 'email']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    # Configuration du formulaire d'édition
    fieldsets = (
        ('Informations Personnelles', {
            'fields': ('nom', 'age', 'sexe', 'email')
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at']
    
    # Fonctions personnalisées pour les statistiques
    def devices_count(self, obj):
        count = obj.devices.count()
        url = reverse('admin:devices_device_changelist') + f'?Patient__id__exact={obj.id}'
        return format_html('<a href="{}">{} Device(s)</a>', url, count)
    devices_count.short_description = 'Devices'
    
    def mesures_count(self, obj):
        count = obj.mesures.count()
        url = reverse('admin:mesures_mesure_changelist') + f'?Patient__id__exact={obj.id}'
        return format_html('<a href="{}">{} Mesure(s)</a>', url, count)
    mesures_count.short_description = 'Mesures'
    
    def alerts_count(self, obj):
        count = obj.alerts.count()
        url = reverse('admin:alerts_alert_changelist') + f'?Patient__id__exact={obj.id}'
        return format_html('<a href="{}">{} Alerte(s)</a>', url, count)
    alerts_count.short_description = 'Alertes'
    
    # Actions personnalisées
    actions = ['export_patients_data']
    
    def export_patients_data(self, request, queryset):
        # Cette action pourrait être implémentée pour exporter les données des patients
        self.message_user(request, f"Export des données pour {queryset.count()} patients préparé.")
    export_patients_data.short_description = "Exporter les données sélectionnées"
    
    # Panneau de statistiques personnalisé
    def changelist_view(self, request, extra_context=None):
        # Ajouter des statistiques au contexte
        stats = {
            'total_patients': Patient.objects.count(),
            'avg_age': Patient.objects.aggregate(avg_age=Avg('age'))['avg_age'] or 0,
            'by_sex': Patient.objects.values('sexe').annotate(count=Count('id')),
            'recent_patients': Patient.objects.order_by('-created_at')[:5]
        }
        
        extra_context = extra_context or {}
        extra_context['stats'] = stats
        
        return super().changelist_view(request, extra_context=extra_context)
