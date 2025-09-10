from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Q
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    # Configuration de la liste
    list_display = ['device_id', 'type_capteur', 'status', 'patient_link', 'mesures_count', 'alerts_count', 'last_activity']
    list_filter = ['type_capteur', 'status', 'Patient__sexe']
    search_fields = ['device_id', 'Patient__nom', 'Patient__email']
    list_editable = ['status']
    ordering = ['-status', 'device_id']
    
    # Configuration du formulaire d'édition
    fieldsets = (
        ('Informations du Device', {
            'fields': ('device_id', 'type_capteur', 'status')
        }),
        ('Patient Associé', {
            'fields': ('Patient',)
        }),
    )
    
    # Fonctions personnalisées pour les liens et statistiques
    def patient_link(self, obj):
        if obj.Patient:
            url = reverse('admin:patients_patient_change', args=[obj.Patient.id])
            return format_html('<a href="{}">{}</a>', url, obj.Patient.nom)
        return "Aucun patient"
    patient_link.short_description = 'Patient'
    
    def mesures_count(self, obj):
        count = obj.mesure_set.count()
        url = reverse('admin:mesures_mesure_changelist') + f'?device__id__exact={obj.id}'
        return format_html('<a href="{}">{} Mesure(s)</a>', url, count)
    mesures_count.short_description = 'Mesures'
    
    def alerts_count(self, obj):
        count = obj.alert_set.count()
        url = reverse('admin:alerts_alert_changelist') + f'?device__id__exact={obj.id}'
        return format_html('<a href="{}">{} Alerte(s)</a>', url, count)
    alerts_count.short_description = 'Alertes'
    
    def last_activity(self, obj):
        # Trouver la dernière mesure pour ce device
        last_mesure = obj.mesure_set.order_by('-timestamp').first()
        if last_mesure:
            return last_mesure.timestamp
        return "Aucune activité"
    last_activity.short_description = 'Dernière activité'
    
    # Actions personnalisées
    actions = ['activate_devices', 'deactivate_devices', 'export_devices_report']
    
    def activate_devices(self, request, queryset):
        updated = queryset.update(status=True)
        self.message_user(request, f"{updated} device(s) activé(s) avec succès.")
    activate_devices.short_description = "Activer les devices sélectionnés"
    
    def deactivate_devices(self, request, queryset):
        updated = queryset.update(status=False)
        self.message_user(request, f"{updated} device(s) désactivé(s) avec succès.")
    deactivate_devices.short_description = "Désactiver les devices sélectionnés"
    
    def export_devices_report(self, request, queryset):
        self.message_user(request, f"Rapport pour {queryset.count()} device(s) généré.")
    export_devices_report.short_description = "Générer un rapport des devices"
    
    # Panneau de statistiques personnalisé
    def changelist_view(self, request, extra_context=None):
        # Statistiques des devices
        stats = {
            'total_devices': Device.objects.count(),
            'active_devices': Device.objects.filter(status=True).count(),
            'inactive_devices': Device.objects.filter(status=False).count(),
            'by_type': Device.objects.values('type_capteur').annotate(count=Count('id')),
            'devices_without_patient': Device.objects.filter(Patient__isnull=True).count(),
        }
        
        extra_context = extra_context or {}
        extra_context['stats'] = stats
        
        return super().changelist_view(request, extra_context=extra_context)
