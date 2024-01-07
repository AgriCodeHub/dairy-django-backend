from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.models import Cow
from inventory.models import CowInventory


@receiver(post_save, sender=Cow)
def update_cow_inventory_on_save(sender, instance, created, **kwargs):
    """
    Signal receiver function to update the cow inventory upon saving a Cow instance.

    Parameters:
    - sender (class): The model class (Cow) that sends the signal.
    - instance (Cow): The instance of the Cow model that triggered the signal.
    - created (bool): A flag indicating whether the instance was created or updated.
    - **kwargs: Additional keyword arguments.

    This function is connected to the post_save signal of the Cow model. When a Cow instance
    is saved, it attempts to retrieve an existing CowInventory object or create a new one if
    it doesn't exist. It then calls the update_cow_inventory function to update the counts
    based on the latest information from the Cow model.

    Example:
    ```python
    cow_instance = Cow.objects.create(name="Bessie", availability_status="Alive", gender="Female")
    ```
    """
    try:
        cow_inventory = CowInventory.objects.get(pk=1)
    except CowInventory.DoesNotExist:
        cow_inventory = CowInventory.objects.create()

    update_cow_inventory(cow_inventory)


@receiver(post_delete, sender=Cow)
def update_cow_inventory_on_delete(sender, instance, **kwargs):
    """
    Signal receiver function to update the cow inventory upon deleting a Cow instance.

    Parameters:
    - sender (class): The model class (Cow) that sends the signal.
    - instance (Cow): The instance of the Cow model that triggered the signal.
    - **kwargs: Additional keyword arguments.

    This function is connected to the post_delete signal of the Cow model. When a Cow instance
    is deleted, it attempts to retrieve an existing CowInventory object or create a new one if
    it doesn't exist. It then calls the update_cow_inventory function to update the counts
    based on the latest information from the Cow model.

    Example:
    ```python
    cow_instance = Cow.objects.get(name="Bessie")
    cow_instance.delete()
    ```
    """
    try:
        cow_inventory = CowInventory.objects.get(pk=1)
    except CowInventory.DoesNotExist:
        cow_inventory = CowInventory.objects.create()

    update_cow_inventory(cow_inventory)


def update_cow_inventory(cow_inventory):
    """
    Update the cow inventory with the latest counts of different cow statuses and genders.

    Parameters:
    - cow_inventory (CowInventory): The CowInventory object to be updated.

    The function retrieves counts of various cow statuses and genders from the Cow model
    and updates the corresponding fields in the provided CowInventory object. The counts
    include the total number of alive cows, the number of male and female alive cows, the
    number of sold cows, and the number of dead cows. After updating the counts, the changes
    are saved to the database.

    Example:
    ```python
    cow_inventory = CowInventory.objects.get(id=1)
    update_cow_inventory(cow_inventory)
    ```
    """
    cow_inventory.total_number_of_cows = Cow.objects.filter(
        availability_status="Alive"
    ).count()
    cow_inventory.number_of_male_cows = Cow.objects.filter(
        availability_status="Alive", gender="Male"
    ).count()
    cow_inventory.number_of_female_cows = Cow.objects.filter(
        availability_status="Alive", gender="Female"
    ).count()
    cow_inventory.number_of_sold_cows = Cow.objects.filter(
        availability_status="Sold"
    ).count()
    cow_inventory.number_of_dead_cows = Cow.objects.filter(
        availability_status="Dead"
    ).count()

    cow_inventory.save()
