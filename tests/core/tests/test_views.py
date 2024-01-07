import pytest
from django.urls import reverse
from rest_framework import status
from core.choices import CowBreedChoices

from core.models import Cow, CowBreed
from core.serializers import CowSerializer, InseminatorSerializer


@pytest.mark.django_db
class TestCowBreedViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users):
        self.client = setup_users["client"]
        self.tokens = {
            "farm_owner": setup_users["farm_owner_token"],
            "farm_manager": setup_users["farm_manager_token"],
            "asst_farm_manager": setup_users["asst_farm_manager_token"],
            "team_leader": setup_users["team_leader_token"],
            "farm_worker": setup_users["farm_worker_token"],
        }

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_201_CREATED),
            ("farm_manager", status.HTTP_201_CREATED),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("team_leader", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_create_cow_breed(self, user_type, expected_status):
        """
        Test creating a cow breed with different user types.
        """
        cow_breed_data = {"name": CowBreedChoices.GUERNSEY}
        response = self.client.post(
            reverse("core:cow-breeds-list"),
            cow_breed_data,
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

        if expected_status == status.HTTP_201_CREATED:
            assert CowBreed.objects.filter(name=cow_breed_data["name"]).exists()

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_200_OK),
            ("farm_manager", status.HTTP_200_OK),
            ("asst_farm_manager", status.HTTP_200_OK),
            ("farm_worker", status.HTTP_200_OK),
        ],
    )
    def test_retrieve_cow_breeds(self, user_type, expected_status):
        """
        Test retrieving cow breeds with different user types.
        """
        response = self.client.get(
            reverse("core:cow-breeds-list"),
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_200_OK),
            ("farm_manager", status.HTTP_200_OK),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("team_leader", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_update_cow_breed(self, user_type, expected_status):
        """
        Test updating a cow breed with different user types.
        """
        cow_breed = CowBreed.objects.create(name=CowBreedChoices.FRIESIAN)
        url = reverse("core:cow-breeds-detail", kwargs={"pk": cow_breed.id})
        cow_breed_update_data = {"name": CowBreedChoices.AYRSHIRE}
        response = self.client.put(
            url,
            cow_breed_update_data,
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_204_NO_CONTENT),
            ("farm_manager", status.HTTP_204_NO_CONTENT),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("team_leader", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_delete_cow_breed(self, user_type, expected_status):
        """
        Test deleting a cow breed with different user types.
        """
        cow_breed = CowBreed.objects.create(name=CowBreedChoices.FRIESIAN)
        url = reverse("core:cow-breeds-detail", kwargs={"pk": cow_breed.id})
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}"
        )
        assert response.status_code == expected_status

        if expected_status == status.HTTP_204_NO_CONTENT:
            assert not CowBreed.objects.filter(id=cow_breed.id).exists()

    @pytest.mark.parametrize(
        "filter_name, expected_count, status_code",
        [
            (CowBreedChoices.JERSEY, 1, status.HTTP_200_OK),
            ("ey", 2, status.HTTP_200_OK),
            ("nonexistent", 1, status.HTTP_404_NOT_FOUND),
        ],
    )
    def test_filter_cow_breeds_by_name(self, filter_name, expected_count, status_code):
        """
        Test filtering cow breeds by name.
        """
        CowBreed.objects.create(name=CowBreedChoices.JERSEY)
        CowBreed.objects.create(name=CowBreedChoices.GUERNSEY)
        url = reverse("core:cow-breeds-list") + f"?name={filter_name}"

        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Token {self.tokens['farm_owner']}"
        )

        assert response.status_code == status_code
        assert len(response.data) == expected_count

    def test_order_cow_breeds_by_multiple_fields(self):
        """
        Test ordering cow breeds by multiple fields.
        """
        CowBreed.objects.create(name=CowBreedChoices.JERSEY)
        CowBreed.objects.create(name=CowBreedChoices.GUERNSEY)
        CowBreed.objects.create(name=CowBreedChoices.CROSSBREED)
        url = reverse("core:cow-breeds-list") + "?ordering=-name"
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Token {self.tokens['farm_manager']}"
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3
        assert response.data[0]["name"] == CowBreedChoices.JERSEY
        assert response.data[1]["name"] == CowBreedChoices.GUERNSEY
        assert response.data[2]["name"] == CowBreedChoices.CROSSBREED

    def test_no_results_for_invalid_name(self):
        """
        Test that no results are returned for an invalid cow breed name.
        """
        url = reverse("core:cow-breeds-list") + "?name=nonexistent"
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Token {self.tokens['farm_worker']}"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {
            "detail": "No cow breed(s) found matching the provided filters."
        }


@pytest.mark.django_db
class TestCowViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users, setup_cows):
        self.client = setup_users["client"]

        self.tokens = {
            "farm_owner": setup_users["farm_owner_token"],
            "farm_manager": setup_users["farm_manager_token"],
            "asst_farm_manager": setup_users["asst_farm_manager_token"],
            "team_leader": setup_users["team_leader_token"],
            "farm_worker": setup_users["farm_worker_token"],
        }
        self.general_cow = setup_cows

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_201_CREATED),
            ("farm_manager", status.HTTP_201_CREATED),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_create_cow(self, user_type, expected_status):
        response = self.client.post(
            reverse("core:cows-list"),
            data=self.general_cow,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status
        if expected_status == status.HTTP_201_CREATED:
            assert Cow.objects.filter(name=self.general_cow["name"]).exists()

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_200_OK),
            ("farm_manager", status.HTTP_200_OK),
            ("asst_farm_manager", status.HTTP_200_OK),
            ("farm_worker", status.HTTP_200_OK),
        ],
    )
    def test_retrieve_cow(self, user_type, expected_status):
        response = self.client.get(
            reverse("core:cows-list"),
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_200_OK),
            ("farm_manager", status.HTTP_200_OK),
            ("asst_farm_manager", status.HTTP_200_OK),
            ("farm_worker", status.HTTP_200_OK),
        ],
    )
    def test_retrieve_cow_detail(self, user_type, expected_status):
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        response = self.client.get(
            reverse("core:cows-detail", kwargs={"pk": cow.pk}),
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status
        assert response.data["name"] == cow.name

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_200_OK),
            ("farm_manager", status.HTTP_200_OK),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_update_cow_detail(self, user_type, expected_status):
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()

        data = {"name": "Updated Cow"}
        response = self.client.patch(
            reverse("core:cows-detail", kwargs={"pk": cow.pk}),
            data=data,
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_204_NO_CONTENT),
            ("farm_manager", status.HTTP_403_FORBIDDEN),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_delete_cow(self, user_type, expected_status):
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()

        response = self.client.delete(
            reverse("core:cows-detail", kwargs={"pk": cow.pk}),
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "filter_field, filter_value, expected_count, status_code",
        [
            ("breed", CowBreedChoices.JERSEY, 1, status.HTTP_200_OK),
            ("is_bought", "True", 1, status.HTTP_404_NOT_FOUND),
            ("gender", "Fem", 1, status.HTTP_200_OK),
            ("year_of_birth", "2019", 1, status.HTTP_404_NOT_FOUND),
            ("month_of_birth", "12", 1, status.HTTP_404_NOT_FOUND),
            ("availability_status", "ALI", 1, status.HTTP_200_OK),
            ("current_pregnancy_status", "pregnant", 1, status.HTTP_404_NOT_FOUND),
            ("category", "dairy", 1, status.HTTP_404_NOT_FOUND),
            ("current_production_status", "Open", 1, status.HTTP_200_OK),
            ("name", "General Cow", 1, status.HTTP_200_OK),
        ],
    )
    def test_filter_cows_by_field(
        self, filter_field, filter_value, expected_count, status_code
    ):
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()

        url = reverse("core:cows-list") + f"?{filter_field}={filter_value}"

        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Token {self.tokens['farm_owner']}"
        )

        assert response.status_code == status_code
        assert len(response.data) == expected_count

    @pytest.mark.parametrize(
        "ordering_field, expected_order",
        [
            ("date_of_birth", ["asc", "desc"]),
            ("name", ["asc", "desc"]),
            ("gender", ["asc", "desc"]),
            ("breed", ["asc", "desc"]),
        ],
    )
    def test_order_cows_by_field(self, ordering_field, expected_order):
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()

        url_asc = reverse("core:cows-list") + f"?ordering={ordering_field}"
        response_asc = self.client.get(
            url_asc, HTTP_AUTHORIZATION=f"Token {self.tokens['farm_owner']}"
        )
        assert response_asc.status_code == status.HTTP_200_OK

        url_desc = reverse("core:cows-list") + f"?ordering=-{ordering_field}"
        response_desc = self.client.get(
            url_desc, HTTP_AUTHORIZATION=f"Token {self.tokens['farm_owner']}"
        )
        assert response_desc.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestInseminatorViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users, setup_inseminators_data):
        self.client = setup_users["client"]

        self.tokens = {
            "farm_owner": setup_users["farm_owner_token"],
            "farm_manager": setup_users["farm_manager_token"],
            "asst_farm_manager": setup_users["asst_farm_manager_token"],
            "team_leader": setup_users["team_leader_token"],
            "farm_worker": setup_users["farm_worker_token"],
        }

        self.inseminators_data = setup_inseminators_data

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_201_CREATED),
            ("farm_manager", status.HTTP_201_CREATED),
            ("asst_farm_manager", status.HTTP_201_CREATED),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_create_inseminator(self, user_type, expected_status):
        response = self.client.post(
            reverse("core:inseminator-records-list"),
            data=self.inseminators_data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_200_OK),
            ("farm_manager", status.HTTP_200_OK),
            ("asst_farm_manager", status.HTTP_200_OK),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_retrieve_inseminator(self, user_type, expected_status):
        response = self.client.get(
            reverse("core:inseminator-records-list"),
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_200_OK),
            ("farm_manager", status.HTTP_200_OK),
            ("asst_farm_manager", status.HTTP_200_OK),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_update_inseminator(self, user_type, expected_status):
        serializer = InseminatorSerializer(data=self.inseminators_data)
        assert serializer.is_valid()
        inseminator = serializer.save()
        updated_license_number = {"license_number": "UPDATED-123-2024"}

        response = self.client.patch(
            reverse("core:inseminator-records-detail", kwargs={"pk": inseminator.pk}),
            data=updated_license_number,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_204_NO_CONTENT),
            ("farm_manager", status.HTTP_204_NO_CONTENT),
            ("asst_farm_manager", status.HTTP_204_NO_CONTENT),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_delete_inseminator(self, user_type, expected_status):
        serializer = InseminatorSerializer(data=self.inseminators_data)
        assert serializer.is_valid()
        inseminator = serializer.save()

        response = self.client.delete(
            reverse("core:inseminator-records-detail", kwargs={"pk": inseminator.pk}),
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status
