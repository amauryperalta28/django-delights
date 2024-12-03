from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ingredients/', views.IngredientsListView.as_view(), name='ingredient_list'),
    path('ingredients/<int:pk>/update/', views.IngredientsUpdateView.as_view(), name='ingredient_update'),
    path('menu/', views.menuitem_list, name='menu'),
    path('purchases/', views.purchases_list, name='purchases'),
    path('profit_revenue/', views.profit_revenue, name='profit_revenue'),
]
