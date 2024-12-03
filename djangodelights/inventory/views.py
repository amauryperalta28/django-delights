from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, CreateView
from .forms import IngredientForm

from .models import Ingredient

# Create your views here.

class IngredientsListView(ListView):
    model = Ingredient
    template_name = 'inventory/ingredient_list.html'
    context_object_name = 'ingredient_list'
    
class IngredientsUpdateView(UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'inventory/ingredient_update_form.html'
    success_url = reverse_lazy('ingredient_list')

class IngredientsCreateView(CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'inventory/ingredient_create.html'
    success_url = reverse_lazy('ingredient_list')

def index(request):
    return render(request, 'inventory/index.html')

def menuitem_list(request):
    return render(request, 'inventory/menu_item_list.html')

def purchases_list(request):
    return render(request, 'inventory/purchases.html')

def profit_revenue(request):
    return render(request, 'inventory/profit_revenue.html')
