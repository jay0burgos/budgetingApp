from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *



# MATH FOR HOME CHART CONTEXTS
def totals(request, category):
    this_total=0
    user = User.objects.get(id = request.session['user_id'])
    for expense in user.expenses.filter(category = category):
        this_total += expense.amount
    return this_total 

# PAGES
def home(request):
    if 'user_id' not in request.session: #redirects to login
        return redirect ('/')
    context={
        'logged_user' : User.objects.get(id=request.session['user_id']),
        'auto_total' : totals(request, "Auto"),
        'education_total' : totals(request,"Education"),
        'entertainment_total' : totals(request,"Entertainment"),
        'food_total' : totals(request,"Food"),
        'home_total' : totals(request, "Home"),
        'utilities_total' : totals(request, "Utilities"),
        'other_total' : totals(request, "Other")
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
