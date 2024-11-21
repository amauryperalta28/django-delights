from django.db import models

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField(null=False, blank=False)
    unit = models.CharField(max_length=8)
    quantity = models.IntegerField(default=1)
    cost = models.FloatField()

class MenuItem(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField(null=False, blank=False)

class RecipeRequirement(models.Model):
    menu_item_id = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    Ingredient_Id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Purchase(models.Model):
    customer_name = models.CharField(max_length=30)
    MenuItemId = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    date = models.DateField()