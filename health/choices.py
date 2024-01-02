from django.db import models


class QuarantineReasonChoices(models.TextChoices):
    SICK_COW = "Sick Cow"
    BOUGHT_COW = "Bought Cow"
    NEW_COW = "New Cow"
    CALVING = "Calving"
