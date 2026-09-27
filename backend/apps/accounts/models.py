import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models import Q

from apps.core.models import TimeStampedModel
from apps.organizations.models import Location, Organization

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    class Meta:
        ordering = ("email",)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self) -> str:
        return self.email


class Permission(TimeStampedModel):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("code",)

    def __str__(self) -> str:
        return self.code


class Role(TimeStampedModel):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="roles",
    )
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission, blank=True, related_name="roles")
    is_system = models.BooleanField(default=False)

    class Meta:
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "name"),
                name="accounts_unique_role_name",
            )
        ]

    def __str__(self) -> str:
        return f"{self.organization.name}: {self.name}"


class Membership(TimeStampedModel):
    class Status(models.TextChoices):
        INVITED = "invited", "Invited"
        ACTIVE = "active", "Active"
        SUSPENDED = "suspended", "Suspended"

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.INVITED)
    roles = models.ManyToManyField(
        Role,
        through="MembershipRole",
        blank=True,
        related_name="memberships",
    )
    locations = models.ManyToManyField(
        Location,
        through="MembershipLocation",
        blank=True,
        related_name="memberships",
    )

    class Meta:
        ordering = ("organization__name", "user__email")
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "user"),
                name="accounts_unique_organization_membership",
            )
        ]

    def permission_codes(self) -> set[str]:
        if self.user.is_superuser:
            return set(Permission.objects.values_list("code", flat=True))
        return set(
            self.roles.filter(permissions__code__isnull=False).values_list(
                "permissions__code", flat=True
            )
        )

    def has_permission(self, code: str) -> bool:
        if self.status != self.Status.ACTIVE:
            return False
        if self.user.is_superuser:
            return True
        return self.roles.filter(permissions__code=code).exists()

    def __str__(self) -> str:
        return f"{self.user.email} @ {self.organization.name}"


class MembershipRole(models.Model):
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("membership", "role"),
                name="accounts_unique_membership_role",
            )
        ]

    def __str__(self) -> str:
        return f"{self.membership} — {self.role.name}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.membership.organization_id != self.role.organization_id:
            raise ValidationError("Membership and role must belong to the same organization.")


class MembershipLocation(models.Model):
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("membership", "location"),
                name="accounts_unique_membership_location",
            )
        ]

    def __str__(self) -> str:
        return f"{self.membership} — {self.location.name}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.membership.organization_id != self.location.organization_id:
            raise ValidationError("Membership and location must belong to the same organization.")


def active_membership(user: User, organization_id: uuid.UUID | str) -> Membership | None:
    return (
        Membership.objects.filter(
            Q(user=user),
            Q(organization_id=organization_id),
            Q(status=Membership.Status.ACTIVE),
            Q(organization__is_active=True),
        )
        .prefetch_related("roles__permissions", "locations")
        .first()
    )

