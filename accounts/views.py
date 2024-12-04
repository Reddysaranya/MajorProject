from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import QueryDict
import json
from urllib.parse import unquote
import urllib
from .models import recipe,gen_ins,FoodItem
import pandas as pd
import joblib
from .ml_models import train_model
from sklearn.model_selection import train_test_split
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


# Create your views here.
def home(request):
    return render(request,'accounts/index.html')
def about(request):
    return render(request,'accounts/about2.html')
def features(request):
    return render(request,'accounts/features.html')
def child_bmi(request):
    return render(request,'accounts/child_bmi.html')
def blog(request):
    return render(request,'accounts/blog.html')
def usermain(request):
    if request.method == 'POST':
        # Get data from POST request
        height = float(request.POST['height'])
        weight = float(request.POST['weight'])
        age = request.POST['age']
        district = request.POST['district']
        gender = request.POST['gender']
        total_calories = float(request.POST['total_calories'])
        activity_level = request.POST['activity_level']
        category = ""


        recipe.objects.filter(category="Normal").update(category="Healthy")
        # Map the entered age to a category
        age_category = map_age_to_category(age)
        print("Mapped Age Category:", age_category)
        #logger.info("Mapped Age Category: %s", age_category)
        


        # ... existing logic remains unchanged, but replace age with age_category where needed
        # Convert age range to average age (update this logic to use age_category)
        if age_category != "N/A":
            age_division = age_category.split('-')
            age_min = float(age_division[0])
            age_max = float(age_division[1])
            bmr_age = (age_min + age_max) / 2
        else:
            bmr_age = 0  # Handle the N/A case accordingly
        # # Convert age range to average age
        # age_divison = age.split('-')
        # age_min = float(age_divison[0])
        # age_max = float(age_divison[1])
        # bmr_age = (age_min + age_max) / 2

        # BMI Calculation
        bmi = weight / ((height / 100) ** 2)

        # Gender-specific BMI category determination
        if gender.lower() == "male":
            if bmi < 18.5:
                category = "Underweight"
            elif bmi > 25.5:
                category = "Overweight"
            else:
                category = "Healthy"
        elif gender.lower() == "female":
            if bmi < 18.5:
                category = "Underweight"
            elif bmi > 25.5:
                category = "Overweight"
            else:
                category = "Healthy"
        else:
            category = "Unknown gender"
        print("the bmi category is : ",category)
        # BMR Calculation
        if gender.lower() == "male":
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * bmr_age)
        elif gender.lower() == "female":
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * bmr_age)
        else:
            bmr = "N/A"

        # Activity factors
        activity_factors = {
            "Sedentary": 1.2,
            "Light": 1.375,
            "Moderate": 1.55,
            "Active": 1.725,
            "Very Active": 1.9,
            "Extra Active": 2.0
        }

        # Get activity factor
        activity_factor = activity_factors.get(activity_level, 1.2)  # Default to sedentary if not found

        # Calculate TDEE
        if isinstance(bmr, (int, float)):
            tdee = bmr * activity_factor
        else:
            tdee = "N/A"

        # Determine message based on BMI category and calorie consumption
        if isinstance(tdee, (int, float)):
            if category == "Underweight":
                if total_calories < tdee:
                    calorie_message = "You are underweight and consuming insufficient calories. You should increase your calorie intake to promote healthy weight gain."
                elif total_calories > tdee:
                    calorie_message = "You are underweight, but you are consuming more calories. Continue with this calorie intake to achieve a healthier weight."
            elif category == "Overweight":
                if total_calories < tdee:
                    calorie_message = "You are overweight, and you are consuming fewer calories. Continue with this calorie deficit to promote weight loss, but make sure it’s gradual and healthy."
                elif total_calories > tdee:
                    calorie_message = "You are overweight and consuming excessive calories. Reduce your calorie intake and exercise more to promote weight loss."
            else:  # For Healthy BMI
                if total_calories < tdee:
                    calorie_message = "You are healthy but consuming fewer calories than required. You should increase your intake to maintain your weight."
                elif total_calories > tdee:
                    calorie_message = "You are healthy but consuming more calories than required. You should reduce your intake to maintain your weight."
                else:
                    calorie_message = "Your calorie intake is perfectly balanced."
        else:
            calorie_message = "Unable to calculate calorie balance due to missing data."

        # Get current date and determine season
        #current_date = datetime.now().date()
        current_date = datetime(2024, 4, 15).date()

        print("\n current date is :",current_date)
        season, mal_instructions = get_season(current_date)


        # Querying database for relevant data
        # if category == "Normal" or category == "Healthy":
        #     category_values = ["Healthy", "Normal"]
        # else:
        #     category_values = [category]
        
        print("\ndistrict= ",district)
        print("\ncategory= ",category)
        print("\n age=",age_category)
        object_1 = recipe.objects.filter(district=district, category=category, age=age_category)
        print("the recipe cat is :", object_1)
        for obj in object_1:
            print("Category for this recipe object:", obj.category) 
        
        object_2 = gen_ins.objects.filter(age=age_category)
        print("category and other values are : ",category,bmr,tdee,object_1,object_2)
        
        # Render the template with additional context
        for obj in object_2:
            return render(request, 'accounts/usermain.html', {
                'obj1': object_1,
                'instructions': obj.instructions,
                'food_items': obj.food_items,
                'mal_instructions': mal_instructions,
                'category': category,
                'season': season,
                'calorie_message': calorie_message,
                'bmr': bmr,
                'tdee': tdee  # Include the message in the context
            })
        print("\nfinal cat is :",category)
        
    # Handle GET request or other logic
    return render(request, 'accounts/usermain.html')
def items_home(request):
    my_data = request.GET.get('data', '')
    object_1=recipe.objects.filter(recipe_name=my_data)
    for obj in object_1:
        return render(request,'accounts/item2.html',{'recipe_name':my_data,'ins':obj.instructions,'calories':obj.calories,'people_served':obj.people_served,'difficulty':obj.difficulty, 'ing':obj.ingredients})

def post1(request):
    return render(request,'accounts/post1.html')
def post2(request):
    return render(request,'accounts/post2.html')
def post3(request):
    return render(request,'accounts/post3.html')
def post4(request):
    return render(request,'accounts/post4.html')
def post5(request):
    return render(request,'accounts/post5.html')
def post6(request):
    return render(request,'accounts/post6.html')

def yoga1(request):
    return render(request,'accounts/yoga1.html')
def yoga2(request):
    return render(request,'accounts/yoga2.html')
def yoga3(request):
    return render(request,'accounts/yoga3.html')
def yoga4(request):
    return render(request,'accounts/yoga4.html')
def bmi(request):
    return render(request,'accounts/bmi.html')
def bmi_predicted(request):
    if request.method == 'POST':
        # Retrieve form data
        model = joblib.load('accounts/linear_regression_model.pkl')
        height = float(request.POST['height'])
        weight = float(request.POST['weight'])
        rice_quantity = int(request.POST['rice'])
        roti_quantity = int(request.POST['roti'])
        dal_quantity = int(request.POST['dal'])
        eggs_quantity = int(request.POST['eggs'])
        sabzi_quantity = int(request.POST['sabzi'])
        fruits_quantity = int(request.POST['fruits'])
        buttermilk_quantity = int(request.POST['buttermilk'])
        juice_quantity = int(request.POST['juice'])
        workout=int(request.POST['workout'])
        # Calculate total nutrients and calories
        total_proteins = rice_quantity * 2.6 + roti_quantity * 3 + dal_quantity * 8.9 + eggs_quantity * 6 + sabzi_quantity * 2 + fruits_quantity * 0.6 + buttermilk_quantity * 2 + juice_quantity * 0.5
        total_fats = rice_quantity * 0.3 + roti_quantity * 1 + dal_quantity * 0.4 + eggs_quantity * 5.3 + sabzi_quantity * 4 + fruits_quantity * 0.5 + buttermilk_quantity * 1.5 + juice_quantity * 0.2
        total_carbohydrates = rice_quantity * 28 + roti_quantity * 15 + dal_quantity * 20 + eggs_quantity * 1.1 + sabzi_quantity * 8 + fruits_quantity * 15 + buttermilk_quantity * 10 + juice_quantity * 25
        total_vitamins = rice_quantity * 0.1 + roti_quantity * 0.2 + dal_quantity * 0.4 + eggs_quantity * 0.1 + sabzi_quantity * 0.2 + fruits_quantity * 0.1 + buttermilk_quantity * 0.3 + juice_quantity * 0.2
        total_minerals = rice_quantity * 0.5 + roti_quantity * 0.3 + dal_quantity * 0.2 + eggs_quantity * 0.1 + sabzi_quantity * 1 + fruits_quantity * 0.3 + buttermilk_quantity * 0.7 + juice_quantity * 0.5
        total_calories = rice_quantity * 130 + roti_quantity * 80 + dal_quantity * 104 + eggs_quantity * 78 + sabzi_quantity * 120 + fruits_quantity * 60 + buttermilk_quantity * 42 + juice_quantity * 100

        # Calculate BMI
        bmi = int(weight / ((height / 100) ** 2))
        protein_percentage = (total_proteins / 1000) * 100
        carbohydrate_percentage = (total_carbohydrates / 5000) * 100
        fat_percentage = (total_fats / 2000) * 100 

        total_nutrients = total_proteins + total_fats + total_carbohydrates + total_vitamins + total_minerals
        protein_percentage2 = (total_proteins / total_nutrients) * 100
        carbohydrate_percentage2 = (total_carbohydrates / total_nutrients) * 100
        fat_percentage2 = (total_fats / total_nutrients) * 100
        vitamin_percentage2 = (total_vitamins / total_nutrients) * 100
        mineral_percentage2 = (total_minerals / total_nutrients) * 100
        # Render results in a new HTML page


        

        # Load your dataset containing BMI values
        # For example, if you have a CSV file with BMI values, you can load it using pandas
        dataset = pd.read_csv('accounts/dataset_2nd_april.csv')

        # Extract the corresponding BMI values from the dataset
        X = dataset.drop('BMI After 30 Days' , axis=1)
        y = dataset['BMI After 30 Days']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # Train the model
        model = train_model(X_train, y_train)

        # Save the trained model
        joblib.dump(model, 'accounts/linear_regression_model.pkl')

        # Make predictions
        predicted_bmi = model.predict([[bmi,total_calories,workout]])
        return render(request, 'accounts/bmi_predicted.html', {
            'bmi': bmi,
            'total_proteins': total_proteins,
            'total_fats': total_fats,
            'total_carbohydrates': total_carbohydrates,
            'total_vitamins': total_vitamins,
            'total_minerals': total_minerals,
            'total_calories': total_calories,
            'protein_percentage': protein_percentage,
            'carbohydrate_percentage': carbohydrate_percentage,
            'fat_percentage': fat_percentage,
            'protein_percentage2': protein_percentage2,
            'carbohydrate_percentage2': carbohydrate_percentage2,
            'fat_percentage2': fat_percentage2,
            'vitamin_percentage2': vitamin_percentage2,
            'mineral_percentage2': mineral_percentage2,
            'workout':workout,
            'predicted_bmi': predicted_bmi[0],
        })

def get_season(date):
    month = date.month
    if month in [12, 1, 2]:
        mal_instructions = "<ul><li>•   Carrots</li><li>•   Spinach</li><li>•   Guavas</li><li>•   Cauliflower</li><li>•   Almonds</li></ul>"
        return "Winter", mal_instructions
    elif month in [3, 4, 5]:
        mal_instructions = "<ul><li>•   Mangoes</li><li>•   Strawberries</li><li>•   Lettuce</li><li>•   Peas</li><li>•   Apricots</li></ul>"
        return "Summer", mal_instructions
    elif month in [6, 7, 8]:
        mal_instructions = "<ul><li>•   Brinjal</li><li>•   Corn</li><li>•   Green Leafy Vegetables</li><li>•    Apples</li><li>•    Grapes</li></ul>"
        return "Monsoon", mal_instructions
    elif month in [9, 10, 11]:
        mal_instructions = "<ul><li>•      Pumpkins</li><li>•      Sweet Potatoes</li><li>•      Taro</li><li>•      Pomegranates</li><li>•      Peppers</li></ul>"
        return "Post-Monsoon/Autumn", mal_instructions
    return "Unknown Season", ""

def map_age_to_category(age):
    try:
        # Remove non-numeric characters and convert to integer
        age = ''.join(filter(str.isdigit, age))
        if not age:  # Check if age is empty after filtering
            return "N/A"
        
        age = int(age)  # Convert input to an integer
        
        if 0 <= age < 1:
            return "0-1"
        elif 1 <= age < 2:
            return "1-2"
        elif 2 <= age < 4:
            return "2-4"
        elif 4 <= age <= 5:
            return "4-5"
        elif 6 <= age <= 10:
            return "6-10"
        elif 11 <= age <= 20:
            return "11-20"
        elif 21 <= age <= 35:
            return "21-35"
        elif 36 <= age <= 45:
            return "36-45"
        else:
            return "N/A"  # Out of defined ranges
    except ValueError:
        return "N/A"  # Handle non-integer input
