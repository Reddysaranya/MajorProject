from django.db import models

class recipe(models.Model):
    

    recipe_name = models.CharField(max_length=100)
    people_served = models.TextField(blank=True)
    calories = models.TextField(blank=True)
    difficulty = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    age = models.CharField(max_length=20, blank=True)
    category = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=50, blank=True)
class gen_ins(models.Model):
    instructions=models.TextField()
    food_items=models.TextField()
    mal_ins=models.TextField()
    age=models.CharField(max_length=20,null=True)

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)
    proteins = models.FloatField()
    vitamins = models.FloatField()
    minerals = models.FloatField()
    carbohydrates = models.FloatField()
    fats = models.FloatField()
    calories = models.FloatField()