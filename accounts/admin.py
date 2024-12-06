from django.contrib import admin
from .models import recipe,gen_ins,FoodItem
# Register your models here.
"""
from .models import Person
admin.site.register(Person)
"""
admin.site.register(recipe)
admin.site.register(gen_ins)
admin.site.register(FoodItem)

from .models import Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'height', 'weight', 'state', 'gender')