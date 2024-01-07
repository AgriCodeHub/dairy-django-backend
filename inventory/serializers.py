from rest_framework import serializers

from inventory.models import CowInventory


class CowInventorySerializer(serializers.ModelSerializer):
    """
    Serializer for the CowInventory model.

    Fields:
    - `total_number_of_cows`: An integer field representing the total number of cows.
    - `number_of_male_cows`: An integer field representing the number of male cows.
    - `number_of_female_cows`: An integer field representing the number of female cows.
    - `number_of_sold_cows`: An integer field representing the number of sold cows.
    - `number_of_dead_cows`: An integer field representing the number of dead cows.
    - `last_update`: A read-only field representing the date and time of the last update.

    Meta:
    - `model`: The CowInventory model for which the serializer is defined.
    - `fields`: The fields to include in the serialized representation.

    Usage:
        Use this serializer to convert CowInventory model instances to JSON representations
        and vice versa.

    Example:
        ```
        class CowInventory(models.Model):
            total_number_of_cows = models.PositiveIntegerField(default=0, editable=False)
            number_of_male_cows = models.PositiveIntegerField(default=0, editable=False)
            number_of_female_cows = models.PositiveIntegerField(default=0, editable=False)
            number_of_sold_cows = models.PositiveIntegerField(default=0, editable=False)
            number_of_dead_cows = models.PositiveIntegerField(default=0, editable=False)
            last_update = models.DateTimeField(auto_now=True)

        class CowInventorySerializer(serializers.ModelSerializer):
            class Meta:
                model = CowInventory
                fields = "__all__"
        ```
    """

    class Meta:
        model = CowInventory
        fields = (
            "total_number_of_cows",
            "number_of_male_cows",
            "number_of_female_cows",
            "number_of_sold_cows",
            "number_of_dead_cows",
        )
