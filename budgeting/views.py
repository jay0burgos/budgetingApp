from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *



# MATH FOR HOME CHART CONTEXTS
def totals(category):
    this_total=0
    for expense in Expense.objects.filter(category = category):
        this_total += expense.amount
    return this_total 

# PAGES
def home(request):
    if 'user_id' not in request.session: #redirects to login
        return redirect ('/')

    total_auto = totals("Auto")
    education = totals("Education")
    entertainment = totals("Entertainment")
    food = totals("Food")
    home_total =totals("Home")
    utilities = totals("Utilities")
    other = totals("Other")
    context={
        'logged_user' : User.objects.get(id=request.session['user_id']),
        'auto_total' : total_auto,
        'education_total' : education,
        'entertainment_total' : entertainment,
        'food_total' : food,
        'home_total' : home_total,
        'utilities_total' : utilities,
        'other_total' : other
    }
    return render (request, 'budgeting/home_page.html', context)

# EXPENSE AND INCOME
def add_expense(request):
    if request.method == "POST":
        errors = Expense.objects.validate(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                print(key, value)
            return redirect ('/home')
        else:
            Expense.objects.add_expense(request.POST)
            return redirect('/home')


def add_income (request):
    if request.method == "POST":
        Income.objects.add_income(request.POST)
        return redirect('/home')
