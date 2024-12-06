from django import forms
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from django.contrib.auth.forms import AuthenticationForm

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
        
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['title', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'})
        }

class RecipeRequirementForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirement
        fields = ['ingredient', 'quantity']
        widgets = {
            'ingredient': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'})
        }

RecipeRequirementFormSet = forms.formset_factory(
    RecipeRequirementForm, 
    extra=3,
    can_delete=True
)

class PurchaseForm(forms.ModelForm):
    MenuItems = forms.ModelMultipleChoiceField(
        queryset=MenuItem.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Menu Items",
    )

    class Meta:
        model = Purchase
        fields = ['customer_name', 'MenuItems']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter menu items to only those with sufficient ingredients
        available_menu_items = []
        for menu_item in self.fields['MenuItems'].queryset:
            recipe_requirements = RecipeRequirement.objects.filter(menuitem=menu_item)
            if all(req.quantity <= req.ingredient.quantity for req in recipe_requirements):
                available_menu_items.append(menu_item)

        self.fields['MenuItems'].queryset = MenuItem.objects.filter(pk__in=[item.pk for item in available_menu_items])
        self.fields['MenuItems'].widget.choices = [
            (item.pk, f"{item.title} - ${item.price:.2f}") for item in self.fields['MenuItems'].queryset
        ]
    
    def calculate_total_price(self):
        """Calculate the total price of selected menu items."""
        total_price = sum(item.price for item in self.cleaned_data.get('MenuItems', []))
        return total_price
    
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )