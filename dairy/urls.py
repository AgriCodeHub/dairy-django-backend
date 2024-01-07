from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Create a schema view for Swagger and ReDoc documentation
schema_view = get_schema_view(
    openapi.Info(
        title="DAIRY MANAGEMENT SYSTEM API",
        default_version="v1",
        description="API for managing dairy-related information",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="agricodehub@gmail.com"),
        license=openapi.License(
            name="Apache License V2.0",
            url="https://www.apache.org/licenses/LICENSE-2.0",
        ),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Define URL patterns for your Django project
urlpatterns = [
    # Include authentication URLs provided by Djoser
    path("auth/", include("djoser.urls")),
    # Include URLs from the 'users' app, and set a namespace for clarity
    path("", include("users.urls", namespace="users")),
    path("core/", include("core.urls", namespace="core")),
    path("reproduction/", include("reproduction.urls", namespace="reproduction")),
    path("production/", include("production.urls", namespace="production")),
    path("health/", include("health.urls", namespace="health")),
    path("inventory/", include("inventory.urls", namespace="inventory")),
    # URL for Swagger documentation with UI
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # URL for ReDoc documentation with UI
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
