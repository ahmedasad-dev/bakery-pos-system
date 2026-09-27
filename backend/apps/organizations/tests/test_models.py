import pytest

from apps.organizations.models import Location, Organization


@pytest.mark.django_db
def test_location_inherits_organization_timezone():
    organization = Organization.objects.create(
        name="North Bakery",
        slug="north-bakery",
        timezone="Asia/Karachi",
    )
    location = Location.objects.create(
        organization=organization,
        name="Main Branch",
        code="MAIN",
    )

    assert location.effective_timezone == "Asia/Karachi"

