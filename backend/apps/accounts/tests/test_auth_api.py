import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

from apps.accounts.models import Membership, Permission, Role, User
from apps.organizations.models import Organization


def prepare_csrf(api_client):
    response = api_client.get(reverse("accounts:csrf"))
    api_client.credentials(HTTP_X_CSRFTOKEN=response.json()["csrfToken"])


@pytest.fixture
def user():
    return User.objects.create_user(
        email="owner@example.com",
        password="a-secure-test-password",
        first_name="Bakery",
        last_name="Owner",
    )


@pytest.mark.django_db
def test_login_sets_http_only_refresh_cookie_and_returns_access_token(api_client, user):
    prepare_csrf(api_client)
    response = api_client.post(
        reverse("accounts:login"),
        {"email": "OWNER@example.com", "password": "a-secure-test-password"},
        format="json",
    )

    assert response.status_code == 200
    AccessToken(response.json()["access"])
    assert response.cookies[settings.JWT_REFRESH_COOKIE_NAME]["httponly"] is True
    assert "refresh" not in response.json()


@pytest.mark.django_db
def test_refresh_rotates_cookie(api_client, user):
    prepare_csrf(api_client)
    login_response = api_client.post(
        reverse("accounts:login"),
        {"email": user.email, "password": "a-secure-test-password"},
        format="json",
    )
    original_refresh = login_response.cookies[settings.JWT_REFRESH_COOKIE_NAME].value
    api_client.cookies[settings.JWT_REFRESH_COOKIE_NAME] = original_refresh

    response = api_client.post(reverse("accounts:refresh"), {}, format="json")

    assert response.status_code == 200
    AccessToken(response.json()["access"])
    assert response.cookies[settings.JWT_REFRESH_COOKIE_NAME].value != original_refresh


@pytest.mark.django_db
def test_me_returns_only_active_memberships(api_client, user):
    prepare_csrf(api_client)
    active_org = Organization.objects.create(name="Active", slug="active")
    inactive_org = Organization.objects.create(name="Inactive", slug="inactive")
    permission = Permission.objects.get(code="organizations.view")
    role = Role.objects.create(organization=active_org, name="Owner")
    role.permissions.add(permission)
    active_membership = Membership.objects.create(
        organization=active_org,
        user=user,
        status=Membership.Status.ACTIVE,
    )
    active_membership.roles.add(role)
    Membership.objects.create(
        organization=inactive_org,
        user=user,
        status=Membership.Status.SUSPENDED,
    )
    token = str(AccessToken.for_user(user))
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = api_client.get(reverse("accounts:me"))

    assert response.status_code == 200
    assert len(response.json()["memberships"]) == 1
    assert response.json()["memberships"][0]["permissions"] == ["organizations.view"]


@pytest.mark.django_db
def test_logout_blacklists_refresh_token(api_client, user):
    prepare_csrf(api_client)
    login_response = api_client.post(
        reverse("accounts:login"),
        {"email": user.email, "password": "a-secure-test-password"},
        format="json",
    )
    api_client.cookies[settings.JWT_REFRESH_COOKIE_NAME] = login_response.cookies[
        settings.JWT_REFRESH_COOKIE_NAME
    ].value

    logout_response = api_client.post(reverse("accounts:logout"), {}, format="json")
    refresh_response = api_client.post(reverse("accounts:refresh"), {}, format="json")

    assert logout_response.status_code == 204
    assert refresh_response.status_code == 204


@pytest.mark.django_db
def test_refresh_without_session_is_a_quiet_no_content_response(api_client):
    prepare_csrf(api_client)

    response = api_client.post(reverse("accounts:refresh"), {}, format="json")

    assert response.status_code == 204


@pytest.mark.django_db
def test_login_rejects_missing_csrf_token(api_client, user):
    response = api_client.post(
        reverse("accounts:login"),
        {"email": user.email, "password": "a-secure-test-password"},
        format="json",
    )

    assert response.status_code == 403

