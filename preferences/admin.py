# preferences/admin.py

from django.contrib import admin
from preferences.models import GrapeRegion

@admin.register(GrapeRegion)
class GrapeRegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'famous_for', 'availability')
    search_fields = ('name', 'country')