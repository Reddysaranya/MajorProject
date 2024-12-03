

import pandas as pd
from django.core.management.base import BaseCommand
from accounts.models import FoodItem

class Command(BaseCommand):
    help = 'Import records from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help=r'C:\Users\nlnsa\Desktop\test\Google_Solutions_challenge_2023-master\accounts\food_item_bmi_predict.xlsx')

    def handle(self, *args, **options):
        file_path = options['file_path']
        
        # Read the Excel file
        df = pd.read_excel(file_path)

        # Iterate over rows and create recipe objects
        for index, row in df.iterrows():
            food_item = FoodItem()
            # Populate model fields with data from CSV row
            food_item.name = row['Food Item']
            food_item.quantity = row['Quantity']
            food_item.proteins = float(row['Proteins (g)'])
            food_item.vitamins = float(row['Vitamins (IU)'])
            food_item.minerals = float(row['Minerals (mg)'])
            food_item.carbohydrates = float(row['Carbohydrates (g)'])
            food_item.fats = float(row['Fats (g)'])
            food_item.calories = float(row['Calories (kcal)'])
            # Save the model object to the database
            food_item.save()
