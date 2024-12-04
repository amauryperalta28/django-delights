from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .forms import IngredientForm, MenuItemForm

from .models import Ingredient, MenuItem, Purchase

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
    
class IngredientsDeleteView(DeleteView):
    model = Ingredient
    template_name = 'inventory/ingredient_delete.html'
    success_url = reverse_lazy('ingredient_list')
    
class MenuItemListView(ListView):
    model  = MenuItem
    template_name = 'inventory/menu_item_list.html'
    context_object_name = 'menu_item_list'

class MenuItemCreateView(CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'inventory/menu_item_create.html'
    success_url = reverse_lazy('menu')
    
class PurchasesListView(ListView):
    model = Purchase
    template_name = 'inventory/purchases.html'
    context_object_name = 'purchases'

def index(request):
    return render(request, 'inventory/index.html')

def menuitem_list(request):
    return render(request, 'inventory/menu_item_list.html')

def purchases_list(request):
    return render(request, 'inventory/purchases.html')

def profit_revenue(request):
    return render(request, 'inventory/profit_revenue.html')
