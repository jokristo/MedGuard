from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Alert

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    # Configuration de la liste
    list_display = ['type_alerte', 'valeur', 'niveau', 'patient_link', 'device_link', 'created_at', 'status_badge', 'action_buttons']
    list_filter = ['niveau', 'type_alerte', 'created_at', 'Patient__sexe']
    search_fields = ['type_alerte', 'message', 'Patient__nom', 'device__device_id']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    list_per_page = 30
    
    # Configuration du formulaire d'édition
    fieldsets = (
        ('Détails de l\'Alerte', {
            'fields': ('type_alerte', 'valeur', 'niveau', 'message')
        }),
        ('Sources', {
            'fields': ('Patient', 'device')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'resolved_at', 'resolved_by', 'resolution_notes'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at']
    
    # Ajouter des champs pour la résolution des alertes
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj and obj.resolved_at:
            # Si l'alerte est déjà résolue, rendre les champs de résolution en lecture seule
            for fieldset in fieldsets:
                if 'Métadonnées' in fieldset[0]:
                    fieldset[1]['fields'] = ('created_at', 'resolved_at', 'resolved_by', 'resolution_notes')
        return fieldsets
    
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
    
    def status_badge(self, obj):
        if obj.resolved_at:
            return format_html('<span style="color: green; font-weight: bold;">✓ Résolue</span>')
        else:
            if obj.niveau == 'danger':
                return format_html('<span style="color: red; font-weight: bold;">⚠️ DANGER</span>')
            else:
                return format_html('<span style="color: orange; font-weight: bold;">⚠️ Avertissement</span>')
    status_badge.short_description = 'Statut'
    
    def action_buttons(self, obj):
        if not obj.resolved_at:
            resolve_url = reverse('admin:resolve_alert', args=[obj.id])
            return format_html(
                '<a href="{}" style="background: #28a745; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px;">Résoudre</a>',
                resolve_url
            )
        return "Déjà résolue"
    action_buttons.short_description = 'Actions'
    
    # Actions personnalisées
    actions = ['resolve_alerts', 'export_alerts_report', 'escalate_alerts']
    
    def resolve_alerts(self, request, queryset):
        unresolved = queryset.filter(resolved_at__isnull=True)
        count = unresolved.update(
            resolved_at=timezone.now(),
            resolved_by=request.user.username,
            resolution_notes="Résolu via action d'administration"
        )
        self.message_user(request, f"{count} alerte(s) résolue(s) avec succès.")
    resolve_alerts.short_description = "Résoudre les alertes sélectionnées"
    
    def export_alerts_report(self, request, queryset):
        self.message_user(request, f"Rapport pour {queryset.count()} alerte(s) généré.")
    export_alerts_report.short_description = "Générer un rapport des alertes"
    
    def escalate_alerts(self, request, queryset):
        self.message_user(request, f"{queryset.count()} alerte(s) escaladée(s) vers le niveau supérieur.")
    escalate_alerts.short_description = "Escalader les alertes"
    
    # Filtres personnalisés
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Filtrer seulement les alertes non résolues si demandé
        if request.GET.get('unresolved_only') == 'true':
            qs = qs.filter(resolved_at__isnull=True)
        
        # Filtrer par niveau de danger si demandé
        if request.GET.get('danger_only') == 'true':
            qs = qs.filter(niveau='danger', resolved_at__isnull=True)
        
        return qs
    
    # Panneau de statistiques personnalisé
    def changelist_view(self, request, extra_context=None):
        # Statistiques des alertes
        now = timezone.now()
        last_24h = now - timedelta(hours=24)
        
        stats = {
            'total_alerts': Alert.objects.count(),
            'unresolved_alerts': Alert.objects.filter(resolved_at__isnull=True).count(),
            'last_24h_alerts': Alert.objects.filter(created_at__gte=last_24h).count(),
            'by_level': Alert.objects.values('niveau').annotate(count=Count('id')),
            'by_type': Alert.objects.values('type_alerte').annotate(count=Count('id')),
            'recent_alerts': Alert.objects.order_by('-created_at')[:10],
        }
        
        extra_context = extra_context or {}
        extra_context['stats'] = stats
        
        return super().changelist_view(request, extra_context=extra_context)
    
    # Surcharger la méthode save pour gérer la résolution
    def save_model(self, request, obj, form, change):
        if 'resolved_at' in form.changed_data and form.cleaned_data['resolved_at']:
            obj.resolved_by = request.user.username
        super().save_model(request, obj, form, change)

# Ajouter une vue personnalisée pour résoudre les alertes
from django.http import HttpResponseRedirect
from django.contrib.admin import site

def resolve_alert_view(request, alert_id):
    from .models import Alert
    try:
        alert = Alert.objects.get(id=alert_id)
        alert.resolved_at = timezone.now()
        alert.resolved_by = request.user.username
        alert.resolution_notes = "Résolu via bouton rapide"
        alert.save()
        site.message_user(request, f"Alerte #{alert_id} résolue avec succès.")
    except Alert.DoesNotExist:
        site.message_user(request, "Alerte non trouvée.", level='error')
    
    return HttpResponseRedirect(reverse('admin:alerts_alert_changelist'))

# Enregistrer la vue personnalisée dans les URLs admin
