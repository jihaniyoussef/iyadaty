from django.contrib import admin

from .models import (NomMedicament, MotifConsultation,
                     ExamenClinique, Posologie, Quantite)


@admin.register(Quantite)
class QuantiteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'created',)
    list_filter = ('created',)
    search_fields = ('nom',)
    date_hierarchy = 'created'
    ordering = ('nom',)


@admin.register(Posologie)
class PosologieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'created',)
    list_filter = ('created',)
    search_fields = ('nom',)
    date_hierarchy = 'created'
    ordering = ('nom',)


@admin.register(NomMedicament)
class NomMedicamentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'dci1', 'dosage')
    list_filter = ('created',)
    search_fields = ('nom',)
    date_hierarchy = 'created'
    ordering = ('nom',)


@admin.register(MotifConsultation)
class MotifConsultationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'created',)
    list_filter = ('created',)
    search_fields = ('nom',)
    date_hierarchy = 'created'
    ordering = ('nom',)


@admin.register(ExamenClinique)
class ExamenCliniqueAdmin(admin.ModelAdmin):
    list_display = ('nom', 'created',)
    list_filter = ('created',)
    search_fields = ('nom',)
    date_hierarchy = 'created'
    ordering = ('nom',)
