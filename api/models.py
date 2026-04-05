from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        VIEWER = 'Viewer', 'Viewer'
        ANALYST = 'Analyst', 'Analyst'
        ADMIN = 'Admin', 'Admin'

    role = models.CharField(
        max_length=7,
        choices=Role.choices,
        default=Role.VIEWER,
    )
    isactive = models.BooleanField(default=True)
    

class Transaction(models.Model):
    class Type(models.TextChoices):
        INCOME = 'Income', 'Income'
        EXPENSE = 'Expense', 'Expense'

    class Category(models.TextChoices):
        SALARY = 'salary', 'Salary'
        FREELANCE = 'freelance', 'Freelance'
        INVESTMENT = 'investment', 'Investment'
        RENT = 'rent', 'Rent'
        FOOD = 'food', 'Food'
        UTILITIES = 'utilities', 'Utilities'
        ENTERTAINMENT = 'entertainment', 'Entertainment'
        HEALTHCARE = 'healthcare', 'Healthcare'
        TRANSPORT = 'transport', 'Transport'
        OTHER = 'other', 'Other'

    user = models.ForeignKey(
    User,
    on_delete=models.PROTECT,
    related_name='transactions'
)
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type_of = models.CharField(max_length=7, choices=Type.choices)
    category = models.CharField(max_length=13, choices=Category.choices)
    date = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class Meta:
    ordering = ['-created_at']
