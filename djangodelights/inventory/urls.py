from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ingredients/', views.ingredients, name='ingredients'),
    path('menu/', views.menu, name='menu'),
    path('purchases/', views.purchases, name='purchases'),
    path('profit_revenue/', views.profit_revenue, name='profit_revenue'),
]
