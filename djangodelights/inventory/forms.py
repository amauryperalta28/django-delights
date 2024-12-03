from django import forms
from .models import Ingredient

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'price', 'unit', 'quantity', 'cost']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingredient name', 'id': 'id_name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'aria-label': 'Price (to the nearest dollar)', 'id': 'id_price', 'min':'0'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingredient unit', 'id': 'id_unit'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingredient quantity', 'id': 'id_quantity'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingredient cost', 'id': 'id_cost'}),
        }
