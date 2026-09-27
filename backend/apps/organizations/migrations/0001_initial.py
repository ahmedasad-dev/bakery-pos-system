# Generated manually for the Phase 1 schema.
import uuid

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Organization",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=160)),
                ("legal_name", models.CharField(blank=True, max_length=200)),
                ("slug", models.SlugField(max_length=80, unique=True)),
                (
                    "default_currency",
                    models.CharField(
                        default="USD",
                        max_length=3,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Currency must be a three-letter ISO 4217 code.",
                                regex="^[A-Z]{3}$",
                            )
                        ],
                    ),
                ),
                ("timezone", models.CharField(default="UTC", max_length=64)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=160)),
                ("code", models.CharField(max_length=32)),
                ("timezone", models.CharField(blank=True, max_length=64)),
                ("address", models.JSONField(blank=True, default=dict)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="locations",
                        to="organizations.organization",
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
                "constraints": [
                    models.UniqueConstraint(
                        fields=("organization", "code"),
                        name="organizations_unique_location_code",
                    )
                ],
            },
        ),
    ]

