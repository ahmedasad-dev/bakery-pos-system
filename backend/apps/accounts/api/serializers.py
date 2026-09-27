from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.accounts.models import Membership, User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False, write_only=True)

    def validate(self, attrs):
        email = attrs["email"].lower()
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=attrs["password"],
        )
        if user is None or not user.is_active:
            raise serializers.ValidationError("Invalid email or password.")
        attrs["user"] = user
        return attrs


class MembershipSerializer(serializers.ModelSerializer):
    organization_id = serializers.UUIDField(read_only=True)
    organization_name = serializers.CharField(source="organization.name", read_only=True)
    role_names = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    location_ids = serializers.SerializerMethodField()

    class Meta:
        model = Membership
        fields = (
            "id",
            "organization_id",
            "organization_name",
            "status",
            "role_names",
            "permissions",
            "location_ids",
        )

    def get_role_names(self, obj: Membership) -> list[str]:
        return list(obj.roles.values_list("name", flat=True))

    def get_permissions(self, obj: Membership) -> list[str]:
        return sorted(obj.permission_codes())

    def get_location_ids(self, obj: Membership) -> list[str]:
        return [str(value) for value in obj.locations.values_list("id", flat=True)]


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    memberships = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "full_name", "memberships")

    def get_memberships(self, obj: User):
        memberships = obj.memberships.filter(
            status=Membership.Status.ACTIVE,
            organization__is_active=True,
        ).select_related("organization")
        return MembershipSerializer(memberships, many=True).data

