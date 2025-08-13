from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
    
class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.description} - ₹{self.amount}"
    



User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    month = models.PositiveIntegerField()  # 1-12
    year = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('user', 'category', 'month', 'year')

    def __str__(self):
        return f"{self.category.name} - {self.month}/{self.year} - {self.amount}"

