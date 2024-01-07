import pytest
from django.urls import reverse
from rest_framework import status

from health.choices import CullingReasonChoices, PathogenChoices
from health.models import Pathogen
from health.serializers import WeightRecordSerializer, CullingRecordSerializer
from health.views import QuarantineRecordSerializer


@pytest.mark.django_db
class TestWeightRecordViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users, setup_weight_record_data):
        self.client = setup_users["client"]
        self.tokens = {
            "farm_owner": setup_users["farm_owner_token"],
            "farm_manager": setup_users["farm_manager_token"],
            "asst_farm_manager": setup_users["asst_farm_manager_token"],
            "team_leader": setup_users["team_leader_token"],
            "farm_worker": setup_users["farm_worker_token"],
        }

        self.weight_data = setup_weight_record_data

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_201_CREATED),
            ("farm_manager", status.HTTP_201_CREATED),
            ("asst_farm_manager", status.HTTP_201_CREATED),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_create_weight_record(self, user_type, expected_status):
        response = self.client.post(
            reverse("health:weight-records-list"),
            data=self.weight_data,
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
    def test_retrieve_weight_record(self, user_type, expected_status):
        response = self.client.get(
            reverse("health:weight-records-list"),
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
    def test_update_weight_record(self, user_type, expected_status):
        serializer = WeightRecordSerializer(data=self.weight_data)
        assert serializer.is_valid()
        weight_record = serializer.save()
        updated_weight = {"weight_in_kgs": 999}

        response = self.client.patch(
            reverse("health:weight-records-detail", kwargs={"pk": weight_record.pk}),
            data=updated_weight,
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
    def test_delete_weight_record(self, user_type, expected_status):
        serializer = WeightRecordSerializer(data=self.weight_data)
        assert serializer.is_valid()
        weight_record = serializer.save()

        response = self.client.delete(
            reverse("health:weight-records-detail", kwargs={"pk": weight_record.pk}),
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status


@pytest.mark.django_db
class TestCullingRecordViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users, setup_culling_record_data):
        self.client = setup_users["client"]
        self.tokens = {
            "farm_owner": setup_users["farm_owner_token"],
            "farm_manager": setup_users["farm_manager_token"],
            "asst_farm_manager": setup_users["asst_farm_manager_token"],
            "team_leader": setup_users["team_leader_token"],
            "farm_worker": setup_users["farm_worker_token"],
        }

        self.culling_data = setup_culling_record_data

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_201_CREATED),
            ("farm_manager", status.HTTP_201_CREATED),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_create_culling_record(self, user_type, expected_status):
        response = self.client.post(
            reverse("health:culling-records-list"),
            data=self.culling_data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_200_OK),
            ("farm_manager", status.HTTP_200_OK),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_retrieve_culling_record(self, user_type, expected_status):
        response = self.client.get(
            reverse("health:culling-records-list"),
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
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
    def test_update_culling_record(self, user_type, expected_status):
        serializer = CullingRecordSerializer(data=self.culling_data)
        assert serializer.is_valid()
        culling_record = serializer.save()
        updated_reason = {"reason": CullingReasonChoices.INJURIES}

        response = self.client.patch(
            reverse("health:culling-records-detail", kwargs={"pk": culling_record.pk}),
            data=updated_reason,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_204_NO_CONTENT),
            ("farm_manager", status.HTTP_204_NO_CONTENT),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_delete_weight_record(self, user_type, expected_status):
        serializer = CullingRecordSerializer(data=self.culling_data)
        assert serializer.is_valid()
        culling_record = serializer.save()

        response = self.client.delete(
            reverse("health:culling-records-detail", kwargs={"pk": culling_record.pk}),
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status


@pytest.mark.django_db
class TestQuarantineRecordViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users, setup_quarantine_record_data):
        self.client = setup_users["client"]
        self.tokens = {
            "farm_owner": setup_users["farm_owner_token"],
            "farm_manager": setup_users["farm_manager_token"],
            "asst_farm_manager": setup_users["asst_farm_manager_token"],
            "team_leader": setup_users["team_leader_token"],
            "farm_worker": setup_users["farm_worker_token"],
        }

        self.quarantine_data = setup_quarantine_record_data

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_201_CREATED),
            ("farm_manager", status.HTTP_201_CREATED),
            ("asst_farm_manager", status.HTTP_201_CREATED),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_create_quarantine_record(self, user_type, expected_status):
        response = self.client.post(
            reverse("health:quarantine-records-list"),
            data=self.quarantine_data,
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
    def test_retrieve_quarantine_record(self, user_type, expected_status):
        response = self.client.get(
            reverse("health:quarantine-records-list"),
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
    def test_update_quarantine_record(self, user_type, expected_status):
        serializer = QuarantineRecordSerializer(data=self.quarantine_data)
        assert serializer.is_valid()
        quarantine_record = serializer.save()
        updated_quarantine = {"notes": "Updated notes"}

        response = self.client.patch(
            reverse(
                "health:quarantine-records-detail", kwargs={"pk": quarantine_record.pk}
            ),
            data=updated_quarantine,
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
    def test_delete_quarantine_record(self, user_type, expected_status):
        serializer = QuarantineRecordSerializer(data=self.quarantine_data)
        assert serializer.is_valid()
        quarantine_record = serializer.save()

        response = self.client.delete(
            reverse(
                "health:quarantine-records-detail", kwargs={"pk": quarantine_record.pk}
            ),
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status


@pytest.mark.django_db
class TestPathogenViewSet:
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
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_create_pathogen(self, user_type, expected_status):
        pathogen_data = {"name": PathogenChoices.BACTERIA}
        response = self.client.post(
            reverse("health:pathogens-list"),
            pathogen_data,
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_200_OK),
            ("farm_manager", status.HTTP_200_OK),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_retrieve_pathogen(self, user_type, expected_status):
        response = self.client.get(
            reverse("health:pathogens-list"),
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_200_OK),
            ("farm_manager", status.HTTP_200_OK),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_update_pathogen(self, user_type, expected_status):
        pathogen = Pathogen.objects.create(name=PathogenChoices.UNKNOWN)
        url = reverse("health:pathogens-detail", kwargs={"pk": pathogen.id})
        pathogen_update_data = {"name": PathogenChoices.FUNGI}
        response = self.client.put(
            url,
            pathogen_update_data,
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_204_NO_CONTENT),
            ("farm_manager", status.HTTP_204_NO_CONTENT),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_delete_pathogen(self, user_type, expected_status):
        pathogen = Pathogen.objects.create(name=PathogenChoices.UNKNOWN)
        url = reverse("health:pathogens-detail", kwargs={"pk": pathogen.id})
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}"
        )
        assert response.status_code == expected_status
