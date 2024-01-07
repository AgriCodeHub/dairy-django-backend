from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from core.models import Cow, CowBreed, Inseminator


class CowBreedSerializer(serializers.ModelSerializer):
    """
    Serializer for the CowBreed model.

    Fields:
    - `name`: A CharField representing the name of the cow breed.

    Meta:
    - `model`: The CowBreed model for which the serializer is defined.
    - `fields`: The fields to include in the serialized representation.

    Usage:
        Use this serializer to convert CowBreed model instances to JSON representations
        and vice versa. It includes the 'name' field of the cow breed.

    """

    class Meta:
        model = CowBreed
        fields = ("name",)


class CowSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cow model.

    Fields:
    - `breed`: A nested serializer field representing the cow breed, using CowBreedSerializer.
    - `tag_number`: A read-only field representing the cow's tag number.
    - `parity`: A read-only field representing the cow's parity.
    - `age`: A read-only field representing the cow's age in days.
    - `age_in_farm`: A read-only field representing the cow's age in days since introduction to the farm.
    - And more...

    Meta:
    - `model`: The Cow model for which the serializer is defined.
    - `fields`: The fields to include in the serialized representation.

    Usage:
        Use this serializer to convert Cow model instances to JSON representations
        and vice versa. It includes nested serialization for the 'breed' field and
        read-only fields for additional information such as tag number and age.

    Methods:
    - `create(validated_data)`: Overrides the default create method to handle nested serialization for the 'breed' field.
    - `update(instance, validated_data)`: Overrides the default update method to exclude certain fields from updating.

    Example:
        ```
        class Cow(models.Model):
            breed = models.ForeignKey(CowBreed, on_delete=models.CASCADE)
            tag_number = models.CharField(max_length=20)
            parity = models.IntegerField()
            age = models.IntegerField()
            age_in_farm = models.IntegerField()

        class CowSerializer(serializers.ModelSerializer):
            breed = CowBreedSerializer()
            tag_number = serializers.ReadOnlyField()
            parity = serializers.ReadOnlyField()
            age = serializers.ReadOnlyField()
            age_in_farm = serializers.ReadOnlyField()

            class Meta:
                model = Cow
                fields = "__all__"
        ```
    """

    breed = CowBreedSerializer()
    tag_number = serializers.ReadOnlyField()
    parity = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    age_in_farm = serializers.ReadOnlyField()

    class Meta:
        model = Cow
        fields = "__all__"

    def create(self, validated_data):
        breed_data = validated_data.pop("breed")
        breed, _ = CowBreed.objects.get_or_create(**breed_data)

        cow = Cow.objects.create(breed=breed, **validated_data)
        return cow

    def update(self, instance, validated_data):
        fields_to_exclude = [
            "breed",
            "gender",
            "sire",
            "dam",
            "is_bought",
            "date_introduced_in_farm",
        ]
        for field in fields_to_exclude:
            validated_data.pop(field, None)
        return super().update(instance, validated_data)


class InseminatorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Inseminator model.

    Fields:
    - `phone_number`: A field representing the phone number of the inseminator.
    - And more...

    Meta:
    - `model`: The Inseminator model for which the serializer is defined.
    - `fields`: The fields to include in the serialized representation.

    Usage:
        Use this serializer to convert Inseminator model instances to JSON representations
        and vice versa. It includes validation for the 'phone_number' field.

    Example:
        ```
        class Inseminator(models.Model):
            first_name = models.CharField(max_length=20)
            last_name = models.CharField(max_length=20)
            phone_number = PhoneNumberField(max_length=15, unique=True)
            sex = models.CharField(choices=SexChoices.choices, max_length=6)
            company = models.CharField(max_length=50, null=True)
            license_number = models.CharField(max_length=25, unique=True, null=True)

        class InseminatorSerializer(serializers.ModelSerializer):
            phone_number = PhoneNumberField()

            class Meta:
                model = Inseminator
                fields = ("first_name", "last_name", "phone_number", "sex", "company", "license_number")
        ```
    """

    phone_number = PhoneNumberField()

    class Meta:
        model = Inseminator
        fields = ("first_name", "last_name", "phone_number", "sex", "company", "license_number")

