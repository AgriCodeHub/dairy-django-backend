from rest_framework import serializers

from core.models import Cow
from health.models import WeightRecord, CullingRecord, QuarantineRecord, Pathogen


class WeightRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for the WeightRecord model.

    Fields:
    - `cow`: A primary key related field representing the cow associated with the weight record.
    - `weight_in_kgs`: A decimal field representing the weight of the cow in kilograms.
    - `date_taken`: A date field representing the date when the weight record was taken.

    Meta:
    - `model`: The WeightRecord model for which the serializer is defined.
    - `fields`: The fields to include in the serialized representation.

    Usage:
        Use this serializer to convert WeightRecord model instances to JSON representations
        and vice versa.

    Example:
        ```
        class WeightRecord(models.Model):
            cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
            weight_in_kgs = models.DecimalField(max_digits=6, decimal_places=2)
            date_taken = models.DateField(auto_now_add=True)

        class WeightRecordSerializer(serializers.ModelSerializer):
            class Meta:
                model = WeightRecord
                fields = ("cow", "weight_in_kgs", "date_taken")
        ```
    """

    cow = serializers.PrimaryKeyRelatedField(queryset=Cow.objects.all())

    class Meta:
        model = WeightRecord
        fields = ("cow", "weight_in_kgs", "date_taken")


class CullingRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for the CullingRecord model.

    Fields:
    - `cow`: A primary key related field representing the cow associated with the culling record.
    - `reason`: A field representing the reason for culling, chosen from predefined choices.
    - `notes`: A text field representing additional notes or comments about the culling.
    - `date_carried`: A date field representing the date when the culling record was created.

    Meta:
    - `model`: The CullingRecord model for which the serializer is defined.
    - `fields`: The fields to include in the serialized representation.

    Usage:
        Use this serializer to convert CullingRecord model instances to JSON representations
        and vice versa.

    Example:
        ```python
        class CullingRecord(models.Model):
            cow = models.OneToOneField(Cow, on_delete=models.CASCADE, related_name="culling_record")
            reason = models.CharField(max_length=35, choices=CullingReasonChoices.choices)
            notes = models.TextField(null=True, max_length=100)
            date_carried = models.DateField(auto_now_add=True)

        class CullingRecordSerializer(serializers.ModelSerializer):
            class Meta:
                model = CullingRecord
                fields = ("cow", "reason", "notes", "date_carried")
        ```

    """

    cow = serializers.PrimaryKeyRelatedField(queryset=Cow.objects.all())

    class Meta:
        model = CullingRecord
        fields = ("cow", "reason", "notes", "date_carried")


class QuarantineRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for the QuarantineRecord model.

    Fields:
    - `cow`: A primary key related field representing the cow associated with the quarantine record.
    - `reason`: A choice field representing the reason for quarantine.
    - `start_date`: A date field representing the start date of the quarantine record.
    - `end_date`: A date field representing the end date of the quarantine record.
    - `notes`: A text field representing optional notes for the quarantine record.

    Meta:
    - `model`: The QuarantineRecord model for which the serializer is defined.
    - `fields`: The fields to include in the serialized representation.

    Usage:
        Use this serializer to convert QuarantineRecord model instances to JSON representations
        and vice versa.

    Example:
        ```
        class QuarantineRecord(models.Model):
            cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name="quarantine_records")
            reason = models.CharField(max_length=35, choices=QuarantineReasonChoices.choices)
            start_date = models.DateField(auto_now_add=True)
            end_date = models.DateField(null=True)
            notes = models.TextField(null=True, max_length=100)

        class QuarantineRecordSerializer(serializers.ModelSerializer):
            class Meta:
                model = QuarantineRecord
                fields = ("cow", "reason", "start_date", "end_date", "notes")
        ```
    """

    cow = serializers.PrimaryKeyRelatedField(queryset=Cow.objects.all())

    class Meta:
        model = QuarantineRecord
        fields = ("cow", "reason", "start_date", "end_date", "notes")


class PathogenSerializer(serializers.ModelSerializer):
    """
    Serializer for the Pathogen model.

    Fields:
    - `name`: A choice field representing the type of pathogen.

    Meta:
    - `model`: The Pathogen model for which the serializer is defined.
    - `fields`: The fields to include in the serialized representation.

    Usage:
        Use this serializer to convert Pathogen model instances to JSON representations
        and vice versa.

    Example:
        ```
        class Pathogen(models.Model):
            name = models.CharField(max_length=10, choices=PathogenChoices.choices)
            # diagnosis_date = models.DateField(auto_now_add=True)

        class PathogenSerializer(serializers.ModelSerializer):
            class Meta:
                model = Pathogen
                fields = ("name",)
        ```
    """

    class Meta:
        model = Pathogen
        fields = ("name",)
