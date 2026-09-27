import pytest
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

from apps.accounts.models import Membership, User
from apps.organizations.models import Organization


@pytest.mark.django_db
def test_organization_list_is_scoped_to_active_membership(api_client):
    user = User.objects.create_user(email="owner@example.com", password="secret")
    visible = Organization.objects.create(name="Visible", slug="visible")
    Organization.objects.create(name="Hidden", slug="hidden")
    Membership.objects.create(
        organization=visible,
        user=user,
        status=Membership.Status.ACTIVE,
    )
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {AccessToken.for_user(user)}")

    response = api_client.get(reverse("organizations:list"))

    assert response.status_code == 200
    assert [organization["name"] for organization in response.json()] == ["Visible"]

