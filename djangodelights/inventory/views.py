from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'inventory/index.html')

def ingredients_list(request):
    return render(request, 'inventory/ingredient_list.html')

def menuitem_list(request):
    return render(request, 'inventory/menu_item_list.html')

def purchases_list(request):
    return render(request, 'inventory/purchases.html')

def profit_revenue(request):
    return render(request, 'inventory/profit_revenue.html')
