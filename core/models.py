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

class CowInventory(models.Model):
    """
    Represents the cow inventory of the dairy farm.

    Attributes:
    - `total_number_of_cows` (PositiveIntegerField): Total number of cows in the inventory.
    - `number_of_male_cows` (PositiveIntegerField): Number of male cows in the inventory.
    - `number_of_female_cows` (PositiveIntegerField): Number of female cows in the inventory.
    - `number_of_sold_cows` (PositiveIntegerField): Number of cows that have been sold.
    - `number_of_dead_cows` (PositiveIntegerField): Number of cows that have died.
    - `last_update` (DateTimeField): Date and time of the last update to the inventory.

    Note:
    This model is designed to automatically update the counts based on changes to the Cow model using a signal handler.
    """
    total_number_of_cows = models.PositiveIntegerField(default=0, editable=False)
    number_of_male_cows = models.PositiveIntegerField(default=0, editable=False)
    number_of_female_cows = models.PositiveIntegerField(default=0, editable=False)
    number_of_sold_cows = models.PositiveIntegerField(default=0, editable=False)
    number_of_dead_cows = models.PositiveIntegerField(default=0, editable=False)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cow Inventory - Total: {self.total_number_of_cows}, Male: {self.number_of_male_cows}, Female: {self.number_of_female_cows}, Sold: {self.number_of_sold_cows}, Dead: {self.number_of_dead_cows}, Last Update: {self.last_update}"