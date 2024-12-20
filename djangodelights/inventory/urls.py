from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomLoginView.as_view(), name='login'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('dashboard/', views.index, name='dashboard'),
    path('ingredients/', views.IngredientsListView.as_view(), name='ingredient_list'),
    path('ingredients/create/', views.IngredientsCreateView.as_view(), name='ingredient_create'),
    path('ingredients/<int:pk>/delete/', views.IngredientsDeleteView.as_view(), name='ingredient_delete'),
    path('ingredients/<int:pk>/update/', views.IngredientsUpdateView.as_view(), name='ingredient_update'),
    path('menu/', views.MenuItemListView.as_view(), name='menu'),
    path('menu/create/', views.MenuItemCreateView.as_view(), name="menu_item_create"),
    path('menu/<int:pk>/update/', views.MenuItemUpdateView.as_view(), name='menu_item_update'),
    path('purchases/', views.PurchasesListView.as_view(), name='purchases'),
    path('purchases/create/', views.create_purchase, name='create_purchase'),
    path('purchases/success', views.purchase_success, name='purchase_success'),
]
