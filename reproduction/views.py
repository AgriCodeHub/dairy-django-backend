from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from reproduction.filters import (
    PregnancyFilterSet,
    HeatFilterSet,
    InseminationFilterSet,
)
from reproduction.models import Pregnancy, Heat, Insemination
from reproduction.serializers import (
    PregnancySerializer,
    HeatSerializer,
    InseminationSerializer,
)
from users.permissions import (
    IsFarmManager,
    IsFarmOwner,
    IsFarmWorker,
    IsAssistantFarmManager,
    IsTeamLeader,
)


class PregnancyViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle operations related to pregnancy records.

    Provides CRUD functionality for pregnancy records.

    Actions:
    - list: Get a list of pregnancy records based on applied filters.
           Returns a 404 response if no pregnancy records match the provided filters,
           and a 200 response with an empty list if there are no pregnancy records in the database.
    - retrieve: Retrieve details of a specific pregnancy record.
    - create: Create a new pregnancy record.
    - update: Update an existing pregnancy record.
    - partial_update: Partially update an existing pregnancy record.
    - destroy: Delete an existing pregnancy record.

    Serializer class used for request/response data: PregnancySerializer.

    Permissions:
    - For 'list', 'retrieve': Accessible to all users (farm workers, team leaders, assistant farm managers, farm managers, farm owners).
    - For 'create', 'update', 'partial_update', 'destroy': Accessible to farm managers and farm owners only.

    """

    queryset = Pregnancy.objects.all()
    serializer_class = PregnancySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PregnancyFilterSet
    ordering_fields = ["-start_date"]

    def get_permissions(self):
        """
        Get the permissions based on the action.

        - For 'create', 'update', 'partial_update', 'destroy':
          Only farm managers or farm owners are allowed.
        - For other actions, accessible to farm workers, team leaders, assistant farm managers,
          farm managers, and farm owners.

        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsFarmManager | IsFarmOwner]
        else:
            permission_classes = [
                IsFarmWorker
                | IsTeamLeader
                | IsAssistantFarmManager
                | IsFarmManager
                | IsFarmOwner
            ]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        """
        List pregnancy records based on applied filters.

        Returns a 404 response if no pregnancy records match the provided filters,
        and a 200 response with an empty list if there are no pregnancy records in the database.

        """
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                # If query parameters are provided, but there are no matching pregnancy records
                return Response(
                    {
                        "detail": "No Pregnancy record(s) found matching the provided filters."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                # If no query parameters are provided, and there are no pregnancy records in the database
                return Response(
                    {"detail": "No Pregnancy records found."}, status=status.HTTP_200_OK
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class HeatViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle operations related to heat observation records.

    Provides CRUD functionality for heat observation records.

    Actions:
    - list: Get a list of heat observation records based on applied filters.
           Returns a 404 response if no heat observation records match the provided filters,
           and a 200 response with an empty list if there are no heat observation records in the database.
    - retrieve: Retrieve details of a specific heat observation record.
    - create: Create a new heat observation record.
    - partial_update: [Not Allowed] Partial updates are not supported for heat observation records.
    - update: [Not Allowed] Updates are not supported for heat observation records.
    - destroy: [Not Allowed] Deletion of heat observation records is not allowed.

    Serializer class used for request/response data: HeatSerializer.

    Permissions:
    - For 'list', 'retrieve': Accessible to all users (farm workers, team leaders, assistant farm managers, farm managers, farm owners).
    - For 'create': Accessible to farm workers, assistant farm managers, farm managers, and farm owners.
    - For 'partial_update', 'update', 'destroy': Not allowed.

    """

    queryset = Heat.objects.all()
    serializer_class = HeatSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = HeatFilterSet
    ordering_fields = ["-observation_time"]

    def get_permissions(self):
        """
        Get the permissions based on the action.

        - For 'list', 'retrieve': Accessible to all users.
        - For 'create': Accessible to farm workers, assistant farm managers, farm managers, and farm owners.
        - For 'partial_update', 'update', 'destroy': Not allowed.

        """
        if self.action == "create":
            permission_classes = [
                IsFarmWorker | IsAssistantFarmManager | IsFarmManager | IsFarmOwner
            ]
        else:
            permission_classes = [IsAssistantFarmManager | IsFarmManager | IsFarmOwner]
        return [permission() for permission in permission_classes]

    def partial_update(self, request, *args, **kwargs):
        """
        [Not Allowed] Partial updates are not supported for heat observation records.

        Returns:
        - 405 Method Not Allowed.

        """
        raise MethodNotAllowed("PATCH")

    def update(self, request, *args, **kwargs):
        """
        [Not Allowed] Updates are not supported for heat observation records.

        Returns:
        - 405 Method Not Allowed.

        """
        raise MethodNotAllowed("PUT")

    def destroy(self, request, *args, **kwargs):
        """
        [Not Allowed] Deletion of heat observation records is not allowed.

        Returns:
        - 405 Method Not Allowed.

        """
        raise MethodNotAllowed("DELETE")

    def list(self, request, *args, **kwargs):
        """
        List heat observation records based on applied filters.

        Returns a 404 response if no heat observation records match the provided filters,
        and a 200 response with an empty list if there are no heat observation records in the database.

        """
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                # If query parameters are provided, but there are no matching heat observation records
                return Response(
                    {"detail": "No heat records found matching the provided filters."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                # If no query parameters are provided, and there are no heat observation records in the database
                return Response(
                    {"detail": "No heat records found in the farm yet."},
                    status=status.HTTP_200_OK,
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class InseminationViewset(viewsets.ModelViewSet):
    """
    ViewSet to handle operations related to insemination records.

    Provides CRUD functionality for insemination records.

    Actions:
    - list: Get a list of insemination records based on applied filters.
           Returns a 404 response if no insemination records match the provided filters,
           and a 200 response with an empty list if there are no insemination records in the database.
    - retrieve: Retrieve details of a specific insemination record.
    - create: Create a new insemination record.
    - partial_update & update : Partially update an existing insemination record.
    - destroy: [Not Allowed] Deletion of insemination records associated with a pregnancy is not allowed.

    Serializer class used for request/response data: InseminationSerializer.

    Permissions:
    - Accessible to Assistant farm managers, farm managers, and farm owners.
    - For 'destroy': Not allowed for insemination records associated with a pregnancy.

    """

    queryset = Insemination.objects.all()
    serializer_class = InseminationSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = InseminationFilterSet
    ordering_fields = ["date_of_insemination", "success", "cow"]
    permission_classes = [IsAssistantFarmManager | IsFarmManager | IsFarmOwner]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                return Response(
                    {
                        "detail": "No Insemination records found matching the provided filters."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                return Response(
                    {"detail": "No Insemination records found."},
                    status=status.HTTP_200_OK,
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially update an existing insemination record.

        Returns:
        - 200 OK with the updated insemination record.

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        [Not Allowed] Deletion of insemination records associated with a pregnancy is not allowed.

        Returns:
        - 405 Method Not Allowed if associated with a pregnancy.
        - 204 No Content if not associated with a pregnancy.

        """
        instance = self.get_object()

        # Check if the insemination record is associated with a pregnancy
        if instance.pregnancy:
            raise PermissionDenied(
                "Deletion not allowed. Insemination record is associated with a pregnancy."
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
