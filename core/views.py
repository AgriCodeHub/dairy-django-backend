from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from core.filters import CowBreedFilterSet, CowFilterSet, InseminatorFilterSet
from core.models import Cow, CowBreed, Inseminator
from core.serializers import CowBreedSerializer, CowSerializer, InseminatorSerializer
from users.permissions import (
    IsFarmOwner,
    IsFarmManager,
    IsAssistantFarmManager,
    IsFarmWorker,
)


class CowBreedViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle operations related to cow breeds.

    Provides CRUD functionality for cow breeds.

    Actions:
    - list: Get a list of cow breeds based on applied filters.
           Returns a 404 response if no cow breeds match the provided filters,
           and a 200 response with an empty list if there are no cow breeds in the database.
    - retrieve: Retrieve details of a specific cow breed.
    - create: Create a new cow breed.
    - update: Update an existing cow breed.
    - partial_update: Partially update an existing cow breed.
    - destroy: Delete an existing cow breed.

    Serializer class used for request/response data: CowBreedSerializer.

    Permissions:
    - For 'list', 'retrieve': Accessible to all users (farm workers, assistant farm managers, farm managers, farm owners).
    - For 'create', 'destroy', 'update', 'partial_update': Accessible to farm managers and farm owners only.

    """

    queryset = CowBreed.objects.all()
    serializer_class = CowBreedSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CowBreedFilterSet
    ordering_fields = ["name"]

    def get_permissions(self):
        """
        Get the permissions based on the action.

        - For 'create', 'destroy', 'update', 'partial_update':
          Only farm managers or farm owners are allowed.
        - For other actions, accessible to farm workers, assistant farm managers,
          farm managers, and farm owners.

        """
        if self.action in ["create", "destroy", "update", "partial_update"]:
            permission_classes = [IsFarmManager | IsFarmOwner]
        else:
            permission_classes = [
                IsFarmWorker | IsAssistantFarmManager | IsFarmManager | IsFarmOwner
            ]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        """
        List cow breeds based on applied filters.

        Returns a 404 response if no cow breeds match the provided filters,
        and a 200 response with an empty list if there are no cow breeds in the database.

        """
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                # If query parameters are provided, but there are no matching cow breeds
                return Response(
                    {"detail": "No cow breed(s) found matching the provided filters."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                # If no query parameters are provided, and there are no cow breeds in the database
                return Response(
                    {"detail": "No cow breeds found in the farm yet."},
                    status=status.HTTP_200_OK,
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CowViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle operations related to cows.

    Provides CRUD functionality for cows.

    Actions:
    - list: Get a list of cow records based on applied filters.
           Returns a 404 response if no cow records match the provided filters,
           and a 200 response with an empty list if there are no cow records in the database.
    - retrieve: Retrieve details of a specific cow record.
    - create: Create a new cow record.
    - update: Update an existing cow record.
    - partial_update: Partially update an existing cow record.
    - destroy: Delete an existing cow record.

    Serializer class used for request/response data: CowSerializer.

    Permissions:
    - For 'list', 'retrieve': Accessible to all users (farm workers, assistant farm managers, farm managers, farm owners).
    - For 'create', 'update', 'partial_update': Accessible to farm managers and farm owners only.

    """

    queryset = Cow.objects.all()
    serializer_class = CowSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CowFilterSet
    ordering_fields = ["date_of_birth", "name", "gender", "breed"]

    def get_permissions(self):
        """
        Get the permissions based on the action.

        - For 'create', 'update', 'partial_update':
          Only farm managers or farm owners are allowed.
        - For other actions, accessible to farm workers, assistant farm managers,
          farm managers, and farm owners.

        """
        if self.action in ["create", "update", "partial_update"]:
            permission_classes = [IsFarmManager | IsFarmOwner]
        elif self.action == "destroy":
            permission_classes = [IsFarmOwner]
        else:
            permission_classes = [
                IsFarmWorker | IsAssistantFarmManager | IsFarmManager | IsFarmOwner
            ]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        """
        List cow records based on applied filters.

        Returns a 404 response if no cow records match the provided filters,
        and a 200 response with an empty list if there are no cow records in the database.

        """
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                # If query parameters are provided, but there are no matching cow records
                return Response(
                    {"detail": "No cow record(s) found matching the provided filters."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                # If no query parameters are provided, and there are no cow records in the database
                return Response(
                    {"detail": "No cow records found in the farm yet."},
                    status=status.HTTP_200_OK,
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class InseminatorViewset(viewsets.ModelViewSet):
    """
    ViewSet to handle operations related to inseminators.

    Provides CRUD functionality for inseminators.

    Actions:
    - list: Get a list of inseminator records based on applied filters.
           Returns a 404 response if no inseminator records match the provided filters,
           and a 200 response with an empty list if there are no inseminator records in the database.
    - retrieve: Retrieve details of a specific inseminator record.
    - create: Create a new inseminator record.
    - update: Update an existing inseminator record.
    - partial_update: Partially update an existing inseminator record.
    - destroy: Delete an existing inseminator record.

    Serializer class used for request/response data: InseminatorSerializer.

    Permissions:
    - Accessible to farm managers and farm owners only.

    """

    queryset = Inseminator.objects.all()
    serializer_class = InseminatorSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = InseminatorFilterSet
    ordering_fields = ["license_number", "first_name", "last_name"]
    permission_classes = [IsAssistantFarmManager | IsFarmManager | IsFarmOwner]

    def list(self, request, *args, **kwargs):
        """
        List inseminator records based on applied filters.

        Returns a 404 response if no inseminator records match the provided filters,
        and a 200 response with an empty list if there are no inseminator records in the database.

        """
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                # If query parameters are provided, but there are no matching inseminator records
                return Response(
                    {"detail": "No Inseminator record(s) found matching the provided filters."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                # If no query parameters are provided, and there are no inseminator records in the database
                return Response(
                    {"detail": "No Inseminator records found."},
                    status=status.HTTP_200_OK,
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

