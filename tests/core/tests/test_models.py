import pytest
from django.core.exceptions import ValidationError

from core.choices import CowBreedChoices
from core.models import CowBreed

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
        assert err.value.code == 'invalid_cow_breed'

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