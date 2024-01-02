from django.db import models

from core.models import Cow
from health.validators import WeightRecordValidator, QuarantineValidator
from health.choices import QuarantineReasonChoices


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
        return f"{self.cow} - Weight: {self.weight_in_kgs} kgs - Date: {self.date_taken}"

    def clean(self):
        """
        Performs validation checks before saving the weight record.

        Raises:
        - `ValidationError`: If weight record validation fails.
        """
        WeightRecordValidator.validate_weight(self.weight_in_kgs)
        WeightRecordValidator.validate_cow_availability_status(self.cow)
        WeightRecordValidator.validate_frequency_of_weight_records(self.date_taken, self.cow)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)

class QuarantineRecord(models.Model):
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
        # Validate the reason for quarantine
        QuarantineValidator.validate_reason(self.reason, self.cow)

        # Validate the date range for start and end dates
        QuarantineValidator.validate_date(self.start_date, self.end_date)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
