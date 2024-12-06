from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Profile

class RegisterForm(UserCreationForm):
    # Fields not directly related to the User model
    height = forms.FloatField(
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Height in centimeters', 'class': 'form-control'}),
        min_value=30,  # Minimum height (cm)
        max_value=300,  # Maximum height (cm)
        error_messages={'required': 'Height is mandatory and has to be filled.', 'min_value': 'Height must be between 30 cm and 300 cm.', 'max_value': 'Height must be between 30 cm and 300 cm.'}
    )
    
    weight = forms.FloatField(
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Weight in kilograms', 'class': 'form-control'}),
        min_value=2,  # Minimum weight (kg)
        max_value=300,  # Maximum weight (kg)
        error_messages={'required': 'Weight is mandatory and has to be filled.', 'min_value': 'Weight must be between 2 kg and 300 kg.', 'max_value': 'Weight must be between 2 kg and 300 kg.'}
    )
    
    state = forms.CharField(
        max_length=50, 
        required=True,
        error_messages={'required': 'State is mandatory and has to be filled.'}
    )
    
    gender = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female')], 
        required=True,
        error_messages={'required': 'Gender is mandatory and has to be selected.'}
    )
    password1 = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
    password2 = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        # Save the User instance
        user = super().save(commit=False)

        if commit:
            user.save()  # Save the user instance first
            
            # Create the associated Profile instance
            Profile.objects.create(
                user=user,
                height=self.cleaned_data['height'],
                weight=self.cleaned_data['weight'],
                state=self.cleaned_data['state'],
                gender=self.cleaned_data['gender']
            )
        return user

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')    
        
        if password1 != password2:
            self.add_error('password2', 'Passwords do not match')

        return cleaned_data
