from django.core.exceptions import ValidationError
from django.db import models
from users.choices import SexChoices
from core.choices import CowAvailabilityChoices, CowPregnancyChoices
from health.choices import QuarantineReasonChoices
from core.models import Cow


class WeightRecordValidator:
    """
    Provides validation methods for weight records associated with cows.

    Methods:
    - `validate_weight(weight_in_kgs)`: Validates the weight of a cow in kilograms.
    - `validate_cow_availability_status(cow)`: Validates the availability status of a cow for recording weight.
    - `validate_frequency_of_weight_records(date_taken, cow)`: Validates the frequency of weight records for a cow.

    """
    @staticmethod
    def validate_weight(weight_in_kgs):
        """
        Validates the weight of a cow in kilograms.

        Args:
        - `weight_in_kgs` (float): The weight of a cow in kilograms.

        Raises:
        - `ValidationError` with codes:
            - "invalid_weight": If the weight is less than 10 kgs or exceeds the maximum allowed weight of 1500 kgs.
        """
        if weight_in_kgs < 10:
            raise ValidationError("A cow cannot weigh less than 10 kgs!", code="invalid_weight")
        if weight_in_kgs > 1500:
            raise ValidationError("A cow's weight cannot exceed 1500 kgs!", code="invalid_weight")

    @staticmethod
    def validate_cow_availability_status(cow):
        """
        Validates the availability status of a cow for recording weight.

        Args:
        - `cow` (Cow): The cow associated with the weight record.

        Raises:
        - `ValidationError` with code "invalid_availability_status": If the cow is not marked as alive.
        """
        if cow.availability_status != CowAvailabilityChoices.ALIVE:
            raise ValidationError(
                f"Weight records are only allowed for cows present in the farm. This cow is marked as: {cow.availability_status}",
                code="invalid_availability_status",
            )

    @staticmethod
    def validate_frequency_of_weight_records(date_taken, cow):
        """
        Validates the frequency of weight records for a cow.

        Args:
        - `date_taken` (Date): The date when the weight record was taken.
        - `cow` (Cow): The cow associated with the weight record.

        Raises:
        - `ValidationError` with code "duplicate_weight_record": If there is more than one weight record for the same cow on the same date.
        """
        from health.models import WeightRecord

        if WeightRecord.objects.filter(cow=cow, date_taken=date_taken).count() > 1:
            raise ValidationError("This cow already has a weight record on this date!", code="duplicate_weight_record")

class QuarantineValidator:
    @staticmethod
    def validate_reason(reason, cow):
        """
        Validate the reason for cow quarantine.

        Parameters:
        - reason (str): The reason for cow quarantine.
        - cow (Cow): The cow to be quarantined.

        Raises:
        - ValidationError: If the validation fails.

        Returns:
        - None
        """
        if reason == QuarantineReasonChoices.CALVING:
            if cow.gender != SexChoices.FEMALE:
                raise ValidationError("Only female cows can be quarantined for 'Calving'.")

            if cow.current_pregnancy_status != CowPregnancyChoices.PREGNANT:
                raise ValidationError("Only pregnant female cows can be quarantined for 'Calving'.")
    @staticmethod
    def validate_date(start_date, end_date):
        """
        Validate the date range for start and end dates.

        Args:
        - start_date (date): The start date of the quarantine.
        - end_date (date or None): The end date of the quarantine.
        - record_id (int or None): The ID of the record being updated.

        Raises:
        - ValidationError: If the date range is invalid.
        """
        if start_date and end_date and start_date > end_date:
            raise ValidationError("End date must be equal to or after the start date.")

