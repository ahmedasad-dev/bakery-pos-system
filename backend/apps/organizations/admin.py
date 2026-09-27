from django.contrib import admin

from .models import Location, Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "default_currency", "timezone", "is_active")
    list_filter = ("is_active", "default_currency")
    search_fields = ("name", "legal_name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "organization", "timezone", "is_active")
    list_filter = ("is_active", "organization")
    search_fields = ("name", "code", "organization__name")

