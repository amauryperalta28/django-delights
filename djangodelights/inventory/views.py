from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .forms import IngredientForm, MenuItemForm, RecipeRequirementFormSet

from .models import Ingredient, MenuItem, Purchase, RecipeRequirement

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
    
class PurchasesListView(ListView):
    model = Purchase
    template_name = 'inventory/purchase_list.html'
    context_object_name = 'purchases'
    
class MenuItemCreateView(View):
    def get(self, request):
        menu_item_form = MenuItemForm()
        recipe_requirement_formset = RecipeRequirementFormSet()
        return render(request, 'inventory/menu_item_create.html', {
            'menu_item_form': menu_item_form,
            'recipe_requirement_formset': recipe_requirement_formset
        })

    def post(self, request):
        menu_item_form = MenuItemForm(request.POST)
        recipe_requirement_formset = RecipeRequirementFormSet(request.POST)

        if menu_item_form.is_valid() and recipe_requirement_formset.is_valid():
            menu_item = menu_item_form.save()

            for form in recipe_requirement_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                    RecipeRequirement.objects.create(
                        menuitem=menu_item,
                        ingredient=form.cleaned_data['ingredient'],
                        quantity=form.cleaned_data['quantity']
                    )

            return redirect('menu')  # Adjust redirect as needed

        return render(request, 'inventory/menu_item_create.html', {
            'menu_item_form': menu_item_form,
            'recipe_requirement_formset': recipe_requirement_formset
        })

class MenuItemUpdateView(View):
    def get(self, request, pk):
        menu_item = get_object_or_404(MenuItem, pk=pk)
        menu_item_form = MenuItemForm(instance=menu_item)
        
        # Populate initial formset with existing recipe requirements
        initial_requirements = [
            {
                'ingredient': req.ingredient,
                'quantity': req.quantity
            } for req in RecipeRequirement.objects.filter(menuitem=menu_item)
        ]
        
        recipe_requirement_formset = RecipeRequirementFormSet(initial=initial_requirements)
        
        return render(request, 'inventory/menu_item_update.html', {
            'menu_item_form': menu_item_form,
            'recipe_requirement_formset': recipe_requirement_formset,
            'menu_item': menu_item
        })

    def post(self, request, pk):
        menu_item = get_object_or_404(MenuItem, pk=pk)
        menu_item_form = MenuItemForm(request.POST, instance=menu_item)
        recipe_requirement_formset = RecipeRequirementFormSet(request.POST)

        if menu_item_form.is_valid() and recipe_requirement_formset.is_valid():
            # Save menu item
            menu_item = menu_item_form.save()

            # Clear existing recipe requirements
            RecipeRequirement.objects.filter(menuitem=menu_item).delete()

            # Create new recipe requirements
            for form in recipe_requirement_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                    RecipeRequirement.objects.create(
                        menuitem=menu_item,
                        ingredient=form.cleaned_data['ingredient'],
                        quantity=form.cleaned_data['quantity']
                    )

            return redirect('menu')  # Adjust redirect as needed

        return render(request, 'inventory/menu_item_update.html', {
            'menu_item_form': menu_item_form,
            'recipe_requirement_formset': recipe_requirement_formset,
            'menu_item': menu_item
        })

def index(request):
    return render(request, 'inventory/index.html')

def profit_revenue(request):
    return render(request, 'inventory/profit_revenue.html')
