import pytest
from django.urls import reverse
from rest_framework import status

from core.serializers import CowSerializer
from inventory.models import CowInventory


@pytest.mark.django_db
class TestCowInventoryViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users, setup_cows):
        self.client = setup_users["client"]

        self.tokens = {
            "farm_owner": setup_users["farm_owner_token"],
            "farm_manager": setup_users["farm_manager_token"],
            "asst_farm_manager": setup_users["asst_farm_manager_token"],
            "farm_worker": setup_users["farm_worker_token"],
        }
        self.general_cow = setup_cows

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_200_OK),
            ("farm_manager", status.HTTP_200_OK),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_list_cow_inventory(self, user_type, expected_status):
        url = reverse("inventory:cow-inventory-list")
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}"
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_405_METHOD_NOT_ALLOWED),
            ("farm_manager", status.HTTP_405_METHOD_NOT_ALLOWED),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_create_cow_inventory(self, user_type, expected_status):
        url = reverse("inventory:cow-inventory-list")
        data = {
            "total_number_of_cows": 100,
            "number_of_male_cows": 50,
            "number_of_female_cows": 50,
            "number_of_sold_cows": 20,
            "number_of_dead_cows": 5,
        }

        response = self.client.post(
            url, data, HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}"
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_405_METHOD_NOT_ALLOWED),
            ("farm_manager", status.HTTP_405_METHOD_NOT_ALLOWED),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_delete_cow_inventory(self, user_type, expected_status):
        # Assuming you have the CowInventory entry created in the previous test
        cow_inventory_url = reverse("inventory:cow-inventory-list")
        cow_inventory_response = self.client.get(
            cow_inventory_url, HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}"
        )
        cow_inventory_id = cow_inventory_response.data.get("id", None)

        serializer = CowSerializer(data=self.general_cow)
        serializer.is_valid()
        serializer.save()

        cow_inventory = CowInventory.objects.get(id=1)

        delete_url = reverse(
            "inventory:cow-inventory-detail", kwargs={"pk": cow_inventory.id}
        )
        response = self.client.delete(
            delete_url, HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}"
        )
        assert response.status_code == expected_status
