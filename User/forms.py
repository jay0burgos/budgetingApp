#use learn platform forms
#look up vids on the user part
#after modding this, begging making the post part of the trip
from django import forms
from .models import User

class createUserForm(forms.ModelForm):
   
    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name', 'email', 'password')

class logIn(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=30, min_length=15)
    
