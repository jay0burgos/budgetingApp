from django.db import models
import re 
import bcrypt
from datetime import date
from django.core.exceptions import ValidationError
from User.models import User



class ExpenseManager(models.Manager):
    def validate(self,postData):
        errors={}
        if len(postData['paid_to'])<1:
            errors['paid_to'] = "Please tell us who you're paying"
        return errors

    def add_expense (self, postData):
        Expense.objects.create(
            paid_to = postData['paid_to'],
            amount = postData['amount'],
            due_date = postData['due_date'],
            category = postData['category'],
            payer = User.objects.get(id=postData['payer'])
        )

class IncomeManager(models.Manager):
    def add_income (self, postData):
        Income.objects.create(
            amount = postData['in_amount'],
            deposit_date = postData['deposit_date'],
            user = User.objects.get(id=postData['user'])
        )
        

class Expense(models.Model):
    paid_to = models.CharField(max_length=255)
    amount = models.FloatField()
    payer = models.ForeignKey(User, related_name=("expenses"), on_delete=models.CASCADE)
    due_date = models.DateField()
    category = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = ExpenseManager()

class Income(models.Model):
    amount = models.FloatField()
    deposit_date = models.DateField()
    user = models.ForeignKey(User, related_name=("earner"), on_delete=models.CASCADE,)
    category = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = IncomeManager()

#going to be used to track monthly budgets for an annoual anaylist(future feature)
class monthlyBudget(models.Model):
    month = models.DateField()
    user = models.ForeignKey(User, related_name="monthlyBudgets", on_delete=models.CASCADE)
    monthlyIncome = models.OneToOneField(Income, on_delete=models.CASCADE)
    monthlyExpenses = models.ForeignKey(Income, related_name="monthlyExpenses", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
