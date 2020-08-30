from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .forms import *
import bcrypt

# returns splash page
def splashPage(request):
    return render(request, 'splashPage.html')



def createNewUser(request):#used to display create new user form and process that form
    
    if request.method == 'POST':
        form = createUserForm(request.POST,request.FILES)
        if form.is_valid():
           newUser = User.objects.register(request.POST, request.FILES)
           request.session['user_id'] = newUser.id
           print(request.session['user_id'])
           return redirect('/home')
        else:
            form = createUserForm()
            return render(request, 'registerUser.html', {"form": form})
    else: #returns registration page with data inputed along with error messages through form
        content = {
            "form": createUserForm
        }
        return render(request, 'registerUser.html', content)



def login(request):
    if request.method == 'POST':
        result = User.objects.authenticate(request.POST['email'], request.POST['password'])
        if result == False:
            messages.error(request, "Invalid email/Password", extra_tags='login')
        else:
            user = User.objects.get(email=request.POST['email'])
            request.session['user_id'] = user.id
            return redirect('/home')
        
    else:
        return render(request,'logInPage.html')

def logout(request):
    request.session.clear()
    
    return redirect('/')

