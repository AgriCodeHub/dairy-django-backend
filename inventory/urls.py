from django.urls import path, include
from rest_framework import routers

from inventory.views import CowInventoryViewSet

app_name = "inventory"


router = routers.DefaultRouter()
router.register(r'cow-inventory', CowInventoryViewSet, basename='cow-inventory')

urlpatterns = [
    path("", include(router.urls)),
]
