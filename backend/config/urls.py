from django.contrib import admin
from django.urls import include, path

from apps.core.health import HealthCheckView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", HealthCheckView.as_view(), name="health"),
    path("api/v1/auth/", include("apps.accounts.api.urls")),
    path("api/v1/organizations/", include("apps.organizations.api.urls")),
]

