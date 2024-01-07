import pytest
from django.core.exceptions import ValidationError

from core.choices import (
    CowBreedChoices,
    CowAvailabilityChoices,
)
from core.models import CowBreed, Cow
from inventory.models import CowInventory

# new import for test_disease_model
from core.models import CowDisease
from datetime import date


@pytest.mark.django_db
class TestCowBreedModel:
    def test_save_breed_with_valid_name(self):
        breed = CowBreed.objects.create(name=CowBreedChoices.JERSEY)
        assert breed.name == CowBreedChoices.JERSEY

    def test_create_breed_with_invalid_name(self):
        with pytest.raises(ValidationError) as err:
            CowBreed.objects.create(name="unknown_breed")
        assert err.value.code == "invalid_cow_breed"

    def test_create_breed_with_duplicate_name(self):
        # Create a breed with a valid name first
        CowBreed.objects.create(name=CowBreedChoices.FRIESIAN)

        # Attempt to create another breed with the same name, should raise ValidationError
        with pytest.raises(ValidationError) as err:
            CowBreed.objects.create(name=CowBreedChoices.FRIESIAN)

        assert err.value.code == 'duplicate_cow_breed'



# a pytest for CowDisease
@pytest.mark.django_db
class TestCowDiseaseModel:
    # Creating a test instance for the related models.
    pathogen = Pathogen.objects.create(name="Pathogen Test For Cow")
    category = CategoryDisease.objects.create(name="Category Test For Cow")
    cow = Cow.objects.create(nam="Test For Cow")
    symptom = Symptoms.objects.create(name="Symptoms Test For Cow")
    treatment = Treatment.objects.create(name="Treatment Test For Cow") 
    
    # Creating Test Instance For A Disease
    disease =  Disease.objects.create(
		name="Test disease",
		pathogen=pathogen,
		category=category,
		date_reported=date.today(),
		is_recovered=False,
	)
    
    # Testing For ManyToMany Relationships
    disease.cows.add(cow)
    disease.symptoms.add(symptom)
    disease.treatments.add(treatment)
    
    assert disease.cows.count() == 1
    assert disease.symptoms.count() == 1
    assert disease.treatments.count() == 1
    
    # We check for validation test
    with pytest.raises(ValidationError, match="recovered_date is required"):
        disease.is_recovered = True
        disease.full.clean()
        
    disease.recovered_date = date.today()
    disease.full.clean()
    
    with pytest.raises(ValidationError, match="recovered_date must be after the date occured"):
        disease.date_reported = date.today()
        disease.recovered_date = date.today()
        disease.full_clean()

        assert err.value.code == "duplicate_cow_breed"


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

