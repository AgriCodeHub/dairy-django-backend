from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from health.filters import WeightRecordFilterSet, CullingRecordFilterSet
from health.models import WeightRecord, CullingRecord
from health.serializers import WeightRecordSerializer, CullingRecordSerializer
from users.permissions import IsFarmManager, IsFarmOwner, IsAssistantFarmManager


class WeightRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle operations related to weight records.

    Provides CRUD functionality for weight records.

    Actions:
    - list: Get a list of weight records based on applied filters.
           Returns a 404 response if no weight records match the provided filters,
           and a 200 response with an empty list if there are no weight records in the database.
    - retrieve: Retrieve details of a specific weight record.
    - create: Create a new weight record.
    - update: Update an existing weight record.
    - partial_update: Partially update an existing weight record.
    - destroy: Delete an existing weight record.

    Serializer class used for request/response data: WeightRecordSerializer.

    Permissions:
    - For 'list', 'retrieve': Accessible to assistant farm managers, farm managers, and farm owners only.
    - For 'create': Accessible to farm workers, assistant farm managers, farm managers, and farm owners.
    - For 'update', 'partial_update', 'destroy': Accessible to farm managers and farm owners only.

    """

    queryset = WeightRecord.objects.all()
    serializer_class = WeightRecordSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = WeightRecordFilterSet
    ordering_fields = ["-date_taken"]
    permission_classes = [IsAssistantFarmManager | IsFarmManager | IsFarmOwner]

    def list(self, request, *args, **kwargs):
        """
        List weight records based on applied filters.

        Returns a 404 response if no weight records match the provided filters,
        and a 200 response with an empty list if there are no weight records in the database.

        """
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                return Response(
                    {
                        "detail": "No Weight records found matching the provided filters."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                return Response(
                    {"detail": "No Weight records found."}, status=status.HTTP_200_OK
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CullingRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle operations related to culling records.

    Provides CRUD functionality for culling records.

    Actions:
    - list: Get a list of culling records based on applied filters.
           Returns a 404 response if no culling records match the provided filters,
           and a 200 response with an empty list if there are no culling records in the database.
    - retrieve: Retrieve details of a specific culling record.
    - create: Create a new culling record.
    - partial_update: Not allowed.
    - update: Not allowed.
    - destroy: Delete an existing culling record.

    Serializer class used for request/response data: CullingRecordSerializer.

    Permissions:
    - For 'list', 'retrieve': Accessible to farm managers and farm owners only.
    - For 'create': Accessible to farm managers and farm owners only.
    - For 'partial_update', 'update', 'destroy': Accessible to farm managers and farm owners only.

    """

    queryset = CullingRecord.objects.all()
    serializer_class = CullingRecordSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CullingRecordFilterSet
    ordering_fields = ["-date_carried"]
    permission_classes = [IsFarmManager | IsFarmOwner]

    def partial_update(self, request, *args, **kwargs):
        """
        Not allowed.

        Raises:
        - MethodNotAllowed: When attempting a partial update.

        """
        raise MethodNotAllowed("PATCH")

    def update(self, request, *args, **kwargs):
        """
        Not allowed.

        Raises:
        - MethodNotAllowed: When attempting a full update.

        """
        raise MethodNotAllowed("PUT")

    def list(self, request, *args, **kwargs):
        """
        List culling records based on applied filters.

        Returns a 404 response if no culling records match the provided filters,
        and a 200 response with an empty list if there are no culling records in the database.

        """
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                return Response(
                    {
                        "detail": "No Culling records found matching the provided filters."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                return Response(
                    {"detail": "No Culling records found."}, status=status.HTTP_200_OK
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
