from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response

from inventory.models import CowInventory
from inventory.serializers import CowInventorySerializer
from users.permissions import IsFarmManager, IsFarmOwner


class CowInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet to handle operations related to cow inventory.

    Provides read-only functionality for cow inventory.

    Actions:
    - list: Get the cow inventory.
           Returns a 200 response with the cow inventory data.

    Serializer class used for response data: CowInventorySerializer.

    Permissions:
    - Accessible to all authenticated users (farm workers, assistant farm managers, farm managers, farm owners).

    """

    queryset = CowInventory.objects.all()
    serializer_class = CowInventorySerializer
    permission_classes = [IsFarmManager | IsFarmOwner]

    def list(self, request, *args, **kwargs):
        """
        Get the cow inventory.

        Returns a 200 response with the cow inventory data.

        """
        cow_inventory = self.get_queryset().first()

        if not cow_inventory:
            # If there is no cow inventory in the database
            return Response(
                {"detail": "No cow inventory found in the farm yet."},
                status=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(cow_inventory)

        return Response(serializer.data, status=status.HTTP_200_OK)