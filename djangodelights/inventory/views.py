from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .forms import IngredientForm, MenuItemForm, RecipeRequirementFormSet

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

# class MenuItemCreateView(CreateView):
#     model = MenuItem
#     form_class = MenuItemForm
#     template_name = 'inventory/menu_item_create.html'
#     success_url = reverse_lazy('menu')
    
class PurchasesListView(ListView):
    model = Purchase
    template_name = 'inventory/purchase_list.html'
    context_object_name = 'purchases'
    
class MenuItemCreateView(View):
    template_name = 'inventory/menu_item_form.html'

    def get(self, request, *args, **kwargs):
        menu_form = MenuItemForm()
        formset = RecipeRequirementFormSet()
        return render(request, self.template_name, {'menu_form': menu_form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        menu_form = MenuItemForm(request.POST)
        formset = RecipeRequirementFormSet(request.POST)
        if menu_form.is_valid() and formset.is_valid():
            menu_item = menu_form.save()
            recipe_requirements = formset.save(commit=False)
            for requirement in recipe_requirements:
                requirement.menuitem = menu_item
                requirement.save()
            return redirect('menu')  # Redirect to a list view or confirmation page
        return render(request, self.template_name, {'menu_form': menu_form, 'formset': formset})

def index(request):
    return render(request, 'inventory/index.html')

def profit_revenue(request):
    return render(request, 'inventory/profit_revenue.html')
