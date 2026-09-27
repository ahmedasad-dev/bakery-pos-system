from django.core.validators import RegexValidator
from django.db import models

from apps.core.models import TimeStampedModel

currency_validator = RegexValidator(
    regex=r"^[A-Z]{3}$",
    message="Currency must be a three-letter ISO 4217 code.",
)


class Organization(TimeStampedModel):
    name = models.CharField(max_length=160)
    legal_name = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=80, unique=True)
    default_currency = models.CharField(
        max_length=3,
        default="USD",
        validators=[currency_validator],
    )
    timezone = models.CharField(max_length=64, default="UTC")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Location(TimeStampedModel):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="locations",
    )
    name = models.CharField(max_length=160)
    code = models.CharField(max_length=32)
    timezone = models.CharField(max_length=64, blank=True)
    address = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "code"),
                name="organizations_unique_location_code",
            )
        ]

    @property
    def effective_timezone(self) -> str:
        return self.timezone or self.organization.timezone

    def __str__(self) -> str:
        return f"{self.organization.name} — {self.name}"

