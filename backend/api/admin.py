from django.contrib import admin
from api.models import *


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    pass


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    pass


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    pass


@admin.register(FoodType)
class FoodTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(AgeType)
class AgeType(admin.ModelAdmin):
    pass

@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    pass
