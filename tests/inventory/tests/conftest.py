from datetime import timedelta
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.choices import (
    CowAvailabilityChoices,
    CowBreedChoices,
    CowCategoryChoices,
    CowPregnancyChoices,
    CowProductionStatusChoices,
)
from users.choices import SexChoices
from core.utils import todays_date


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
def setup_cows():
    """
    Fixture to create a sample cows object for testing.
    """

    general_cow = {
        "name": "General Cow",
        "breed": {"name": CowBreedChoices.JERSEY},
        "date_of_birth": todays_date - timedelta(days=370),
        "gender": SexChoices.FEMALE,
        "availability_status": CowAvailabilityChoices.ALIVE,
        "current_pregnancy_status": CowPregnancyChoices.OPEN,
        "category": CowCategoryChoices.HEIFER,
        "current_production_status": CowProductionStatusChoices.OPEN,
    }
    return general_cow
