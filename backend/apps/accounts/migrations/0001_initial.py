# Generated manually for the Phase 1 schema.
import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import apps.accounts.managers


def seed_permissions(apps, schema_editor):
    Permission = apps.get_model("accounts", "Permission")
    permissions = (
        ("organizations.view", "View organization settings"),
        ("organizations.manage", "Manage organization settings"),
        ("locations.manage", "Manage locations"),
        ("users.view", "View users and memberships"),
        ("users.manage", "Manage users and memberships"),
        ("roles.manage", "Manage roles and permissions"),
    )
    Permission.objects.bulk_create(
        [Permission(code=code, name=name) for code, name in permissions],
        ignore_conflicts=True,
    )


def unseed_permissions(apps, schema_editor):
    Permission = apps.get_model("accounts", "Permission")
    Permission.objects.filter(
        code__in=(
            "organizations.view",
            "organizations.manage",
            "locations.manage",
            "users.view",
            "users.manage",
            "roles.manage",
        )
    ).delete()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("organizations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("first_name", models.CharField(max_length=80)),
                ("last_name", models.CharField(max_length=80)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text=(
                            "The groups this user belongs to. A user will get all permissions "
                            "granted to each of their groups."
                        ),
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={"ordering": ("email",)},
            managers=[("objects", apps.accounts.managers.UserManager())],
        ),
        migrations.CreateModel(
            name="Permission",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("code", models.CharField(max_length=100, unique=True)),
                ("name", models.CharField(max_length=160)),
                ("description", models.TextField(blank=True)),
            ],
            options={"ordering": ("code",)},
        ),
        migrations.CreateModel(
            name="Role",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=80)),
                ("description", models.TextField(blank=True)),
                ("is_system", models.BooleanField(default=False)),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="roles",
                        to="organizations.organization",
                    ),
                ),
                (
                    "permissions",
                    models.ManyToManyField(blank=True, related_name="roles", to="accounts.permission"),
                ),
            ],
            options={
                "ordering": ("name",),
                "constraints": [
                    models.UniqueConstraint(
                        fields=("organization", "name"), name="accounts_unique_role_name"
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="Membership",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("invited", "Invited"),
                            ("active", "Active"),
                            ("suspended", "Suspended"),
                        ],
                        default="invited",
                        max_length=16,
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="memberships",
                        to="organizations.organization",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="memberships",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("organization__name", "user__email"),
                "constraints": [
                    models.UniqueConstraint(
                        fields=("organization", "user"),
                        name="accounts_unique_organization_membership",
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="MembershipRole",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "membership",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="accounts.membership"),
                ),
                (
                    "role",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="accounts.role"),
                ),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(
                        fields=("membership", "role"), name="accounts_unique_membership_role"
                    )
                ]
            },
        ),
        migrations.CreateModel(
            name="MembershipLocation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "location",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="organizations.location"),
                ),
                (
                    "membership",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="accounts.membership"),
                ),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(
                        fields=("membership", "location"),
                        name="accounts_unique_membership_location",
                    )
                ]
            },
        ),
        migrations.AddField(
            model_name="membership",
            name="locations",
            field=models.ManyToManyField(
                blank=True,
                related_name="memberships",
                through="accounts.MembershipLocation",
                to="organizations.location",
            ),
        ),
        migrations.AddField(
            model_name="membership",
            name="roles",
            field=models.ManyToManyField(
                blank=True,
                related_name="memberships",
                through="accounts.MembershipRole",
                to="accounts.role",
            ),
        ),
        migrations.RunPython(seed_permissions, unseed_permissions),
    ]

