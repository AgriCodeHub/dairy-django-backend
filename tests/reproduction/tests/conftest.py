from datetime import timedelta

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.choices import CowBreedChoices, CowAvailabilityChoices, CowPregnancyChoices, CowCategoryChoices, \
    CowProductionStatusChoices
from core.serializers import CowSerializer, InseminatorSerializer
from core.utils import todays_date
from reproduction.choices import PregnancyStatusChoices
from reproduction.serializers import HeatSerializer
from users.choices import SexChoices


@pytest.fixture()
@pytest.mark.django_db
def setup_users():
    client = APIClient()

    # Create farm owner user
    farm_owner_data = {
        "username": "owner@example.com",
        "email": "abc1@gmail.com",
        "password": "testpassword",
        "first_name": "Farm",
        "last_name": "Owner",
        "phone_number": "+254787654321",
        "sex": SexChoices.MALE,
        "is_farm_owner": True,
    }
    farm_owner_login_data = {
        "username": "owner@example.com",
        "password": "testpassword",
    }
    response = client.post("/auth/users/", farm_owner_data)

    # Retrieve the token after login
    response = client.post(reverse("users:login"), farm_owner_login_data)
    farm_owner_token = response.data["auth_token"]

    # Create farm manager user
    farm_manager_data = {
        "username": "manager@example.com",
        "email": "abc2@gmail.com",
        "password": "testpassword",
        "first_name": "Farm",
        "last_name": "Manager",
        "phone_number": "+254755555555",
        "sex": SexChoices.MALE,
        "is_farm_manager": True,
    }
    farm_manager_login_data = {
        "username": "manager@example.com",
        "password": "testpassword",
    }
    response = client.post("/auth/users/", farm_manager_data)

    # Retrieve the token after login
    response = client.post(reverse("users:login"), farm_manager_login_data)
    farm_manager_token = response.data["auth_token"]

    # Create assistant farm manager user
    asst_farm_manager_data = {
        "username": "assistant@example.com",
        "email": "abc3@gmail.com",
        "password": "testpassword",
        "first_name": "Assistant",
        "last_name": "Farm Manager",
        "phone_number": "+254744444444",
        "sex": SexChoices.FEMALE,
        "is_assistant_farm_manager": True,
    }
    asst_farm_manager_login_data = {
        "username": "assistant@example.com",
        "password": "testpassword",
    }
    response = client.post("/auth/users/", asst_farm_manager_data)

    # Retrieve the token after login
    response = client.post(reverse("users:login"), asst_farm_manager_login_data)
    asst_farm_manager_token = response.data["auth_token"]

    # Create team leader user
    team_leader_data = {
        "username": "leader@example.com",
        "email": "abc4@gmail.com",
        "password": "testpassword",
        "first_name": "Team",
        "last_name": "Leader",
        "phone_number": "+254733333333",
        "sex": SexChoices.MALE,
        "is_team_leader": True,
    }
    team_leader_login_data = {
        "username": "leader@example.com",
        "password": "testpassword",
    }
    response = client.post("/auth/users/", team_leader_data)

    # Retrieve the token after login
    response = client.post(reverse("users:login"), team_leader_login_data)
    assert response.status_code == status.HTTP_200_OK
    team_leader_token = response.data["auth_token"]

    # Create farm worker user
    farm_worker_data = {
        "username": "worker@example.com",
        "email": "abc5@gmail.com",
        "password": "testpassword",
        "first_name": "Farm",
        "last_name": "Worker",
        "phone_number": "+254722222222",
        "sex": SexChoices.FEMALE,
        "is_farm_worker": True,
    }
    farm_worker_login_data = {
        "username": "worker@example.com",
        "password": "testpassword",
    }
    response = client.post("/auth/users/", farm_worker_data)

    # Retrieve the token after login
    response = client.post(reverse("users:login"), farm_worker_login_data)
    farm_worker_token = response.data["auth_token"]

    return {
        "client": client,
        "farm_owner_token": farm_owner_token,
        "farm_manager_token": farm_manager_token,
        "asst_farm_manager_token": asst_farm_manager_token,
        "team_leader_token": team_leader_token,
        "farm_worker_token": farm_worker_token,
    }


@pytest.fixture
@pytest.mark.django_db
def setup_pregnancy_data():
    general_cow = {
        "name": "General Cow",
        "breed": {"name": CowBreedChoices.AYRSHIRE},
        "date_of_birth": todays_date - timedelta(days=650),
        "gender": SexChoices.FEMALE,
        "availability_status": CowAvailabilityChoices.ALIVE,
        "current_pregnancy_status": CowPregnancyChoices.OPEN,
        "category": CowCategoryChoices.HEIFER,
        "current_production_status": CowProductionStatusChoices.OPEN,
    }

    serializer = CowSerializer(data=general_cow)
    assert serializer.is_valid()
    cow = serializer.save()

    pregnancy_data = {"cow": cow.id, "pregnancy_status": PregnancyStatusChoices.CONFIRMED,
                      "start_date": todays_date - timedelta(days=270)}
    return pregnancy_data


@pytest.fixture
def setup_cows():
    """
    Fixture to create a sample cows object for testing.
    """
    general_cow = {
        "name": "General Cow",
        "breed": {"name": CowBreedChoices.AYRSHIRE},
        "date_of_birth": todays_date - timedelta(days=370),
        "gender": SexChoices.FEMALE,
        "availability_status": CowAvailabilityChoices.ALIVE,
        "current_pregnancy_status": CowPregnancyChoices.OPEN,
        "category": CowCategoryChoices.HEIFER,
        "current_production_status": CowProductionStatusChoices.OPEN,
    }
    return general_cow


@pytest.fixture
@pytest.mark.django_db
def setup_insemination_data():
    inseminators_data = {
        "first_name": "Peter",
        "last_name": "Evance",
        "phone_number": "+254712345678",
        "sex": SexChoices.MALE,
        "company": "Peter's Breeders",
        "license_number": "ABC-2023",
    }
    serializer1 = InseminatorSerializer(data=inseminators_data)
    assert serializer1.is_valid()
    inseminator = serializer1.save()

    general_cow = {
        "name": "General Cow",
        "breed": {"name": CowBreedChoices.AYRSHIRE},
        "date_of_birth": todays_date - timedelta(days=366),
        "gender": SexChoices.FEMALE,
        "availability_status": CowAvailabilityChoices.ALIVE,
        "current_pregnancy_status": CowPregnancyChoices.OPEN,
        "category": CowCategoryChoices.HEIFER,
        "current_production_status": CowProductionStatusChoices.OPEN,
    }

    serializer2 = CowSerializer(data=general_cow)
    assert serializer2.is_valid()
    cow = serializer2.save()

    heat_data = {"cow": cow.id}

    serializer3 = HeatSerializer(data=heat_data)
    assert serializer3.is_valid()
    serializer3.save()

    insemination_data = {
        "cow": cow.id,
        "inseminator": inseminator.id,
    }
    return insemination_data
