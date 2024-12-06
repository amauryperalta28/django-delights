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
    

    def calculate_cost(self):
         # Fetch the related recipe requirements
        recipe_requirements = RecipeRequirement.objects.filter(menuitem=self.pk)
        
        # Calculate total ingredient cost
        total_ingredient_cost = sum(
            req.quantity * req.ingredient.cost for req in recipe_requirements
        )
        return total_ingredient_cost
    

class RecipeRequirement(models.Model):
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

# models.py
class Purchase(models.Model):
    customer_name = models.CharField(max_length=30)
    MenuItems = models.ManyToManyField(MenuItem)  # Updated to allow multiple items
    date = models.DateTimeField()

    def __str__(self):
        return f"Purchase by {self.customer_name} on {self.date.strftime('%Y-%m-%d')}"

    def calculate_profit(self):
        total_profit = 0
        for menu_item in self.MenuItems.all():
            recipe_requirements = RecipeRequirement.objects.filter(menuitem=menu_item)
            total_ingredient_cost = sum(
                req.quantity * req.ingredient.cost for req in recipe_requirements
            )
            total_profit += menu_item.price - total_ingredient_cost
        return total_profit

    def calculate_cost(self):
        total_cost = 0
        for menu_item in self.MenuItems.all():
            recipe_requirements = RecipeRequirement.objects.filter(menuitem=menu_item)
            total_ingredient_cost = sum(
                req.quantity * req.ingredient.cost for req in recipe_requirements
            )
            total_cost += total_ingredient_cost
        return total_cost

