from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from core.choices import (
    CowAvailabilityChoices,
    CowBreedChoices,
    CowCategoryChoices,
    CowPregnancyChoices,
    CowProductionStatusChoices,
)
from core.managers import CowManager
from core.validators import CowValidator, CowBreedValidator
from users.choices import SexChoices

# new imports
from datetime import date


class CowBreed(models.Model):
    """
    CowBreed Model

    Represents the breed of a cow in a Django application.

    Attributes:
    - name (CharField): The name of the cow breed.
        Choices are limited to the values defined in CowBreedChoices.

    """

    name = models.CharField(
        max_length=20,
        choices=CowBreedChoices.choices,
    )

    def save(self, *args, **kwargs):
        CowBreedValidator.validate_breed_name(self.name)
        super().save(*args, **kwargs)


class Cow(models.Model):
    """
    Represents an individual cow in the dairy farm.

    Attributes:
    - `name` (str): The name of the cow.
    - `breed` (CowBreed): The breed of the cow.
    - `date_of_birth` (date): The birthdate of the cow.
    - `gender` (str): The gender of the cow.
    - `availability_status` (str): The availability status of the cow.
    - `sire` (Cow or None): The sire (father) of the cow.
    - `dam` (Cow or None): The dam (mother) of the cow.
    - `current_pregnancy_status` (str): The current pregnancy status of the cow.
    - `category` (str): The category of the cow.
    - `current_production_status` (str): The current production status of the cow.
    - `date_introduced_in_farm` (date): The date the cow was introduced to the farm.
    - `is_bought` (bool): Indicates whether the cow was bought or not.
    - `date_of_death` (date or None): The date of death of the cow, if applicable.
    """

    name = models.CharField(max_length=35)
    breed = models.ForeignKey(CowBreed, on_delete=models.PROTECT, related_name="cows")
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=6, choices=SexChoices.choices)
    availability_status = models.CharField(
        choices=CowAvailabilityChoices.choices,
        default=CowAvailabilityChoices.ALIVE,
        max_length=5,
    )
    current_pregnancy_status = models.CharField(
        choices=CowPregnancyChoices.choices,
        default=CowPregnancyChoices.UNAVAILABLE,
        max_length=12,
    )
    category = models.CharField(
        choices=CowCategoryChoices.choices,
        default=CowCategoryChoices.CALF,
        max_length=11,
    )
    current_production_status = models.CharField(
        choices=CowProductionStatusChoices.choices,
        max_length=22,
        default=CowProductionStatusChoices.CALF,
    )
    is_bought = models.BooleanField(default=False)
    sire = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, related_name="offspring"
    )
    dam = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, related_name="calves"
    )
    date_introduced_in_farm = models.DateField(auto_now=True)

    date_of_death = models.DateField(null=True)

    objects = CowManager()

    @property
    def tag_number(self):
        """
        Returns the tag number of the cow.
        """
        return Cow.objects.get_tag_number(self)

    @property
    def age(self):
        """
        Calculates and returns the age of the cow in days.
        """
        return Cow.objects.calculate_age(self)

    @property
    def age_in_farm(self):
        """
        Calculates and returns the age of the cow in days since introduction to the farm.
        """
        return Cow.objects.calculate_age_in_farm(self)

    @property
    def parity(self):
        """
        Calculates and returns the parity of the cow.
        """
        return Cow.objects.calculate_parity(self)

    @property
    def calf_records(self):
        return Cow.objects.get_calf_records(self)

    def clean(self):
        """
        Performs validation checks before saving the cow.

        Raises:
        - `ValidationError`: If cow validation fails.

        """

        if self.pk:
            CowValidator.validate_production_status_2(
                self.current_production_status,
                self.gender,
                self.category,
                self.age,
                self.calf_records,
                self.is_bought,
                self,
            )
            CowValidator.validate_age_category(
                self.age,
                self.category,
                self.gender,
                self.calf_records,
                self.is_bought,
                self,
            )
        else:
            CowValidator.validate_pregnancy_status(
                self,
                self.age,
                self.current_pregnancy_status,
                self.availability_status,
                self.gender,
            )
            CowValidator.validate_uniqueness(self.name)
            CowValidator.validate_cow_age(self.age, self.date_of_birth)
            CowValidator.validate_gender_update(self.pk, self.gender)
            CowValidator.validate_sire_dam_relationship(self.sire, self.dam)
            CowValidator.validate_production_status_1(
                self.current_production_status,
                self.gender,
                self.age,
            )
            CowValidator.validate_pregnancy_status(
                self,
                self.age,
                self.current_pregnancy_status,
                self.availability_status,
                self.gender,
            )

            CowValidator.validate_date_of_death(
                self.availability_status, self.date_of_death
            )

    def __str__(self):
        """
        Returns a string representation of the cow.
        """
        return self.tag_number

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)


class Inseminator(models.Model):
    """
    Represents an individual inseminator involved in the breeding process.

    Attributes:
    - `first_name` (str): The first name of the inseminator.
    - `last_name` (str): The last name of the inseminator.
    - `phone_number` (str): The phone number of the inseminator (unique).
    - `sex` (str): The gender of the inseminator.
    - `company` (str): The company or affiliation of the inseminator (nullable).
    - `license_number` (str): The license number of the inseminator (unique, nullable).

    Methods:
    - `__str__`: Returns a string representation of the inseminator.

    Usage:
        Use this class to represent and manage information about inseminators involved in the breeding process.
    """
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = PhoneNumberField(max_length=15, unique=True)
    sex = models.CharField(choices=SexChoices.choices, max_length=6)
    company = models.CharField(max_length=50, null=True)
    license_number = models.CharField(max_length=25, unique=True, null=True)

    def __str__(self):
        """
        Returns a string representation of the inseminator.
        """
        return f"{self.first_name} {self.last_name}"



class CowDisease(models.Model):
    """
    Represents disease in individual cow.
    
    Attributes:
    - `name` (str): The name of the disease.
    - `pathogen` (ForeignKey): The pathogen associated with the disease.
    - `category` (ForeignKey to DiseaseCategory): The category to which the disease belongs.
	- `date_reported` (Date, auto_now_add=True): The date when the disease is reported.
	- `is_recovered	 (BooleanField, default=False): Indicates whether the disease is recovered.
	- `recovered_date` (Date, editable=False, blank=True, null=True): The date when the disease is marked as recovered.
	- `notes` (TextField, blank=True): Additional notes related to the disease.


	Relationships:
	- `cows` (ManyToManyField to Cow, related_name="diseases"): The cows affected by the disease.
	- `symptoms` (ManyToManyField to Symptoms, related_name="diseases"): The symptoms associated with the disease.
	- `treatments` (ManyToManyField to Treatment, related_name="diseases"): The treatments applied for the disease.

	Usage:
	- Use the model class to represent the Disease for each cow.

    """
    name = models.CharField(max_length=255, unique=True)
    pathogen = models.ForeignKey(Pathogen, on_delete=models.PROTECT)
    category = models.ForeignKey(CategoryDisease, on_delete=models.PROTECT)
    date_reported = models.DateField(auto_now_add=True)
    is_recovered = models.BooleanField(default=False)
    recovered_date = models.DateField(editable=False, blank=True, null=True)
    notes = models.TextField(blank=True)
    cows = models.ManyToManyField(Cow, related_name="diseases")
    symptoms = models.ManyToManyField(Symptoms, related_name="diseases")
    treatments = models.ManyToManyField(Treatment, related_name="diseases")
    
    
    # used the clean function to do validation checks.
    def clean(self):
        # Checking for Validations using the IF statements
        if self.is_recovered and not self.recovered_date:
            raise models.ValidationError("If a disease is marked as recovered, a recovered date is required.")
        
        elif self.recovered_date and not self.is_recovered:
            raise models.ValidationError("If a recovered date is provided, the disease must be marked as recovered.")
        
        elif self.recovered_date and not self.date_reported:
            raise modelsl.ValidationError("The recovered date is after the occurrence date.")
        
        elif self.date_reported > date.today():
            raise models.ValidationError("The occurrence date is not in the future.")
        
        elif not self.name or not self.pathogen:
            raise models.ValidationError("The presence of the disease name and associated pathogen.")
        
        elif self.is_recovered and not self.treatments.exist():
            raise models.ValidationError("If a disease is recovered, at least one treatment is required.")
        
        