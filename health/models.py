from django.db import models

from core.models import Cow
from health.choices import (
    CullingReasonChoices,
    QuarantineReasonChoices,
    PathogenChoices,
    DiseaseCategoryChoices,
    SymptomSeverityChoices,
    SymptomTypeChoices,
    SymptomLocationChoices,
)
from health.validators import (
    PathogenValidator,
    WeightRecordValidator,
    QuarantineValidator,
    DiseaseCategoryValidator,
    SymptomValidator,
)


class WeightRecord(models.Model):
    """
    Represents a weight record for a cow.

    Attributes:
    - `cow` (Cow): The cow associated with the weight record.
    - `weight_in_kgs` (Decimal): The weight of the cow in kilograms.
    - `date_taken` (Date): The date when the weight record was taken.

    Methods:
    - `__str__`: Returns a string representation of the weight record.
    - `clean`: Performs validation checks before saving the weight record.
    - `save`: Overrides the save method to ensure validation before saving.

    Raises:
    - `ValidationError`: If weight record validation fails.
    """

    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    weight_in_kgs = models.DecimalField(max_digits=6, decimal_places=2)
    date_taken = models.DateField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the weight record.
        """
        return (
            f"{self.cow} - Weight: {self.weight_in_kgs} kgs - Date: {self.date_taken}"
        )

    def clean(self):
        """
        Performs validation checks before saving the weight record.

        Raises:
        - `ValidationError`: If weight record validation fails.
        """
        WeightRecordValidator.validate_weight(self.weight_in_kgs)
        WeightRecordValidator.validate_cow_availability_status(self.cow)
        WeightRecordValidator.validate_frequency_of_weight_records(
            self.date_taken, self.cow
        )

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)


class CullingRecord(models.Model):
    """
    Represents a culling record for a cow.

    Attributes:
    - `cow` (Cow): The cow associated with the culling record.
    - `reason` (str): The reason for culling, chosen from predefined choices.
    - `notes` (str): Additional notes or comments about the culling.
    - `date_carried` (Date): The date when the culling record was created.

    Methods:
    - `__str__`: Returns a string representation of the culling record.
    """

    cow = models.OneToOneField(
        Cow, on_delete=models.CASCADE, related_name="culling_record"
    )
    reason = models.CharField(max_length=35, choices=CullingReasonChoices.choices)
    notes = models.TextField(null=True, max_length=100)
    date_carried = models.DateField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the culling record.
        """
        return f"CullingRecord for {self.cow} - Reason: {self.reason} - Date: {self.date_carried}"


class QuarantineRecord(models.Model):
    """
    Represents a quarantine record for a cow.

    Attributes:
    - `cow` (Cow): The cow associated with the quarantine record.
    - `reason` (str): The reason for quarantine, chosen from predefined choices.
    - `start_date` (Date): The start date of the quarantine period.
    - `end_date` (Date): The end date of the quarantine period (optional).
    - `notes` (str): Additional notes or comments about the quarantine.

    Methods:
    - `__str__`: Returns a string representation of the quarantine record.
    - `clean`: Validates the reason for quarantine and the date range.
    - `save`: Overrides the save method to perform additional validation before saving.
    """

    class Meta:
        get_latest_by = "-start_date"

    cow = models.ForeignKey(
        Cow, on_delete=models.CASCADE, related_name="quarantine_records"
    )
    reason = models.CharField(max_length=35, choices=QuarantineReasonChoices.choices)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True)
    notes = models.TextField(null=True, max_length=100)

    def __str__(self):
        if self.end_date:
            return f"Quarantine Record of {self.cow.tag_number} from {self.start_date} to {self.end_date}"
        return f"Quarantine Record of {self.cow.tag_number} from {self.start_date}"

    def clean(self):
        """
        Validate the reason for quarantine and the date range for start and end dates.
        """
        # Validate the reason for quarantine
        QuarantineValidator.validate_reason(self.reason, self.cow)

        # Validate the date range for start and end dates
        QuarantineValidator.validate_date(self.start_date, self.end_date)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to perform additional validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)


class Pathogen(models.Model):
    """
    Represents a pathogen affecting a cow.

    Attributes:
    - `name` (str): The type of pathogen, chosen from predefined choices.

    Methods:
    - `clean`: Validates the name of the pathogen.
    """

    name = models.CharField(max_length=10, choices=PathogenChoices.choices, unique=True)
    # diagnosis_date = models.DateField(auto_now_add=True)

    def clean(self):
        """
        Validate the name of the pathogen.
        """
        PathogenValidator.validate_name(self.name)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to perform additional validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)


class DiseaseCategory(models.Model):
    """
    Represents a category of diseases affecting cows.

    Attributes:
    - `name` (str): The name of the disease category, chosen from predefined choices.

    Methods:
    - `clean`: Validates the name of the disease category.
    """

    name = models.CharField(
        max_length=15, choices=DiseaseCategoryChoices.choices, unique=True
    )

    def clean(self):
        """
        Validate the name of the disease category.
        """
        DiseaseCategoryValidator.validate_name(self.name)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Overrides the save method to perform additional validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)


class Symptoms(models.Model):
    """
    Represents symptoms reported in cows.

    Attributes:
    - `name` (str): The name of the symptom.
    - `symptom_type` (str): The type of the symptom, chosen from predefined choices.
    - `description` (str): Description of the symptom (nullable).
    - `date_observed` (date): Date when the symptom was observed.
    - `severity` (str): Severity of the symptom, chosen from predefined choices.
    - `location` (str): Location of the symptom, chosen from predefined choices.

    Methods:
    - `clean`: Validates the attributes of the symptom.
    """

    name = models.CharField(max_length=50)
    symptom_type = models.CharField(max_length=20, choices=SymptomTypeChoices.choices)
    description = models.TextField(null=True)
    severity = models.CharField(max_length=20, choices=SymptomSeverityChoices.choices)
    location = models.CharField(max_length=20, choices=SymptomLocationChoices.choices)
    date_observed = models.DateField()

    def clean(self):
        """
        Validates the attributes of the symptom.
        """
        SymptomValidator.validate_name(self.name)
        SymptomValidator.validate_fields(
            self.date_observed, self.symptom_type, self.severity, self.location
        )
        SymptomValidator.validate_type_and_location_compatibility(
            self.symptom_type, self.location
        )

    def __str__(self):
        return f" {self.name} reported as #{self.severity} - on #{self.date_observed}"

    def save(self, *args, **kwargs):
        """
        Overrides the save method to perform additional validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)
