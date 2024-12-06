from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.db.models import Sum
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import ListView, View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .forms import IngredientForm, MenuItemForm, RecipeRequirementFormSet, PurchaseForm,CustomLoginForm
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement

# Create your views here.

class IngredientsListView(LoginRequiredMixin,ListView):
    model = Ingredient
    template_name = 'inventory/ingredient_list.html'
    context_object_name = 'ingredient_list'
    
class IngredientsUpdateView(LoginRequiredMixin,UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'inventory/ingredient_update_form.html'
    success_url = reverse_lazy('ingredient_list')

class IngredientsCreateView(LoginRequiredMixin,CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'inventory/ingredient_create.html'
    success_url = reverse_lazy('ingredient_list')
    
class IngredientsDeleteView(LoginRequiredMixin,DeleteView):
    model = Ingredient
    template_name = 'inventory/ingredient_delete.html'
    success_url = reverse_lazy('ingredient_list')
    
class MenuItemListView(LoginRequiredMixin,ListView):
    model  = MenuItem
    template_name = 'inventory/menu_item_list.html'
    context_object_name = 'menu_item_list'
    
class PurchasesListView(LoginRequiredMixin,ListView):
    model = Purchase
    template_name = 'inventory/purchase_list.html'
    context_object_name = 'purchases'
    
class MenuItemCreateView(LoginRequiredMixin, View):
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

class MenuItemUpdateView(LoginRequiredMixin, View):
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

class CustomLoginView(LoginView):
    template_name = 'inventory/auth/login.html'
    form_class = CustomLoginForm

def custom_logout(request):
    # Log out the user
    logout(request)
    
    # Show a success message
    messages.success(request, "You have successfully logged out.")
    
    # Redirect to the login page
    return redirect('login')  #

@login_required
def index(request):
    purchases = Purchase.objects.all()
    revenue = Purchase.objects.annotate(
    total_price=Sum('MenuItems__price')
).aggregate(total_revenue=Sum('total_price'))['total_revenue']
    total_profit = sum(purchase.calculate_profit() for purchase in purchases)
    total_cost = sum(purchase.calculate_cost() for purchase in purchases)

    data = {
        'revenue': revenue,
        'total_profit': total_profit,
        'total_cost': total_cost,
        
    }
   
    return render(request, 'inventory/index.html', {'data': data})

@login_required
def purchase_success(request):
    return render(request, 'inventory/purchase_success.html')

@login_required
def create_purchase(request):
    total_price = 0  # Default value for total price

    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            # Calculate the total price of selected menu items
            total_price = form.calculate_total_price()

            # Validate and process each selected menu item
            menu_items = form.cleaned_data['MenuItems']
            insufficient_ingredients = []
            for menu_item in menu_items:
                recipe_requirements = RecipeRequirement.objects.filter(menuitem=menu_item)
                if not all(req.quantity <= req.ingredient.quantity for req in recipe_requirements):
                    insufficient_ingredients.append(menu_item.title)
            
            if insufficient_ingredients:
                form.add_error(
                    'MenuItems',
                    f"Not enough ingredients to prepare: {', '.join(insufficient_ingredients)}."
                )
            else:
                # Deduct ingredients and create the purchase
                for menu_item in menu_items:
                    recipe_requirements = RecipeRequirement.objects.filter(menuitem=menu_item)
                    for req in recipe_requirements:
                        req.ingredient.quantity -= req.quantity
                        req.ingredient.save()
                
                purchase = form.save(commit=False)
                purchase.date = now()
                purchase.save()
                form.save_m2m()  # Save the many-to-many relationship

                return redirect('purchase_success')  # Replace with your success URL
    else:
        form = PurchaseForm()

    return render(request, 'inventory/purchase_create.html', {
        'form': form,
        'total_price': total_price,  # Pass the total price to the template
    })
