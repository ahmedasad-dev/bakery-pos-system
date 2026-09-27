from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.accounts.models import Membership
from apps.organizations.models import Organization

from .serializers import OrganizationSerializer


class OrganizationQuerySetMixin:
    def get_queryset(self):
        return (
            Organization.objects.filter(
                memberships__user=self.request.user,
                memberships__status=Membership.Status.ACTIVE,
                is_active=True,
            )
            .prefetch_related("locations")
            .distinct()
        )


class OrganizationListView(OrganizationQuerySetMixin, ListAPIView):
    serializer_class = OrganizationSerializer


class OrganizationDetailView(OrganizationQuerySetMixin, RetrieveAPIView):
    serializer_class = OrganizationSerializer

