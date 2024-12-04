from django.db import models

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField(null=False, blank=False)
    unit = models.CharField(max_length=8)
    quantity = models.IntegerField(default=1)
    cost = models.FloatField()
        
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    title = models.CharField(max_length=30)
    price = models.FloatField(null=False, blank=False)
        
    def __str__(self):
        return self.title

class RecipeRequirement(models.Model):
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Purchase(models.Model):
    customer_name = models.CharField(max_length=30)
    MenuItemId = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    date = models.DateTimeField()
    
    def __str__(self):
        return self.MenuItemId.title
