from rest_framework import serializers

from apps.organizations.models import Location, Organization


class LocationSerializer(serializers.ModelSerializer):
    effective_timezone = serializers.CharField(read_only=True)

    class Meta:
        model = Location
        fields = (
            "id",
            "name",
            "code",
            "timezone",
            "effective_timezone",
            "address",
            "is_active",
        )


class OrganizationSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "legal_name",
            "slug",
            "default_currency",
            "timezone",
            "is_active",
            "locations",
        )

