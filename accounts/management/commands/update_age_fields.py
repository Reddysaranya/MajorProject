from django.core.management.base import BaseCommand
from accounts.models import recipe

class Command(BaseCommand):
    help = "Update age fields in the recipe table"

    def handle(self, *args, **kwargs):
        # Mapping of incorrect date formats to age categories
        date_to_age_map = {
            "2024-02-01 00:00:00": "1-2",
            "2024-04-02 00:00:00": "2-4",
            "2024-05-04 00:00:00": "4-5",
            "2024-10-06 00:00:00": "6-10",
        }

        # Fetch all recipes with incorrect age fields
        recipes_to_update = recipe.objects.filter(age__in=date_to_age_map.keys())
        self.stdout.write(f"Found {recipes_to_update.count()} recipes to update.")

        # Update the age field
        for obj in recipes_to_update:
            obj.age = date_to_age_map[obj.age]
            obj.save()
            self.stdout.write(f"Updated recipe ID {obj.id}: age set to {obj.age}")

        self.stdout.write("Age fields updated successfully.")
