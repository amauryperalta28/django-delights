from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ingredients/', views.IngredientsListView.as_view(), name='ingredient_list'),
    path('ingredients/create/', views.IngredientsCreateView.as_view(), name='ingredient_create'),
    path('ingredients/<int:pk>/delete/', views.IngredientsDeleteView.as_view(), name='ingredient_delete'),
    path('ingredients/<int:pk>/update/', views.IngredientsUpdateView.as_view(), name='ingredient_update'),
    path('menu/', views.MenuItemListView.as_view(), name='menu'),
    path('menu/create/', views.MenuItemCreateView.as_view(), name="menu_item_create"),
    path('purchases/', views.PurchasesListView.as_view(), name='purchases'),
    path('profit_revenue/', views.profit_revenue, name='profit_revenue'),
]
