import pytest
from django.core.exceptions import ValidationError

from apps.accounts.models import Membership, MembershipRole, Permission, Role, User
from apps.organizations.models import Organization


@pytest.mark.django_db
def test_membership_permission_is_derived_from_role():
    user = User.objects.create_user(email="cashier@example.com", password="secret")
    organization = Organization.objects.create(name="Bakery", slug="bakery")
    membership = Membership.objects.create(
        organization=organization,
        user=user,
        status=Membership.Status.ACTIVE,
    )
    role = Role.objects.create(organization=organization, name="Manager")
    permission = Permission.objects.get(code="users.view")
    role.permissions.add(permission)
    membership.roles.add(role)

    assert membership.has_permission("users.view") is True
    assert membership.has_permission("users.manage") is False


@pytest.mark.django_db
def test_role_from_another_organization_cannot_be_assigned():
    user = User.objects.create_user(email="cashier@example.com", password="secret")
    first = Organization.objects.create(name="First", slug="first")
    second = Organization.objects.create(name="Second", slug="second")
    membership = Membership.objects.create(
        organization=first,
        user=user,
        status=Membership.Status.ACTIVE,
    )
    foreign_role = Role.objects.create(organization=second, name="Owner")

    with pytest.raises(ValidationError):
        MembershipRole.objects.create(membership=membership, role=foreign_role)

