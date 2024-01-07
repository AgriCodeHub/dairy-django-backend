import pytest

from core.choices import CowBreedChoices, CowAvailabilityChoices
from core.models import CowBreed, Cow
from inventory.models import CowInventory


@pytest.mark.django_db
class TestCowInventoryModel:
    @pytest.fixture(autouse=True)
    def setup(self, setup_cows):
        self.cow_data = setup_cows
        self.cow_data["breed"] = CowBreed.objects.create(name=CowBreedChoices.JERSEY)

    def test_cow_inventory_creation(self):
        # Create a new cow
        Cow.objects.create(**self.cow_data)

        # Check if CowInventory is updated
        cow_inventory = CowInventory.objects.first()
        assert cow_inventory.total_number_of_cows == 1
        assert cow_inventory.number_of_male_cows == 0
        assert cow_inventory.number_of_female_cows == 1
        assert cow_inventory.number_of_sold_cows == 0
        assert cow_inventory.number_of_dead_cows == 0

    def test_cow_inventory_update_on_cow_creation(self):
        # Create a new cow
        Cow.objects.create(**self.cow_data)

        # Check if CowInventory is updated
        cow_inventory = CowInventory.objects.first()
        assert cow_inventory.total_number_of_cows == 1
        assert cow_inventory.number_of_male_cows == 0
        assert cow_inventory.number_of_female_cows == 1
        assert cow_inventory.number_of_sold_cows == 0
        assert cow_inventory.number_of_dead_cows == 0

    def test_cow_inventory_update_on_cow_update(self):
        # Create a new cow
        cow = Cow.objects.create(**self.cow_data)

        # Update the cow
        cow.name = "UpdatedCow"
        cow.availability_status = CowAvailabilityChoices.SOLD
        cow.save()

        # Check if CowInventory is updated
        cow_inventory = CowInventory.objects.first()
        assert cow_inventory.total_number_of_cows == 0
        assert cow_inventory.number_of_male_cows == 0
        assert cow_inventory.number_of_female_cows == 0
        assert cow_inventory.number_of_sold_cows == 1
        assert cow_inventory.number_of_dead_cows == 0

    def test_cow_inventory_update_on_cow_sold(self):
        # Create a new cow
        cow = Cow.objects.create(**self.cow_data)

        # Sell the cow
        cow.availability_status = CowAvailabilityChoices.SOLD
        cow.save()

        # Check if CowInventory is updated
        cow_inventory = CowInventory.objects.first()
        assert cow_inventory.total_number_of_cows == 0
        assert cow_inventory.number_of_male_cows == 0
        assert cow_inventory.number_of_female_cows == 0
        assert cow_inventory.number_of_sold_cows == 1
        assert cow_inventory.number_of_dead_cows == 0

    def test_cow_inventory_update_on_cow_dead(self):
        # Create a new cow
        cow = Cow.objects.create(**self.cow_data)

        # Mark the cow as dead
        cow.availability_status = CowAvailabilityChoices.DEAD
        cow.save()

        # Check if CowInventory is updated
        cow_inventory = CowInventory.objects.first()
        assert cow_inventory.total_number_of_cows == 0
        assert cow_inventory.number_of_male_cows == 0
        assert cow_inventory.number_of_female_cows == 0
        assert cow_inventory.number_of_sold_cows == 0
        assert cow_inventory.number_of_dead_cows == 1

    def test_cow_inventory_update_on_cow_delete(self):
        # Create a new cow
        cow = Cow.objects.create(**self.cow_data)

        # Delete the cow
        cow.delete()

        # Check if CowInventory is updated
        cow_inventory = CowInventory.objects.first()
        assert cow_inventory.total_number_of_cows == 0
        assert cow_inventory.number_of_male_cows == 0
        assert cow_inventory.number_of_female_cows == 0
        assert cow_inventory.number_of_sold_cows == 0
        assert cow_inventory.number_of_dead_cows == 0
