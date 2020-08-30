from django.db import models
from datetime import datetime
import bcrypt


class UserManager(models.Manager):
    def get_all_by_email(self):
        return self.order_by('email')

    def register(self, form_data, newAvatar):#addimagefile: #creates the new user
        my_hash = bcrypt.hashpw(form_data['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            avatar = newAvatar['avatar'],
            first_name=form_data['first_name'],
            last_name=form_data['last_name'],
            password=my_hash,
            email=form_data['email'],
        )

    def authenticate(self, email, password):
        # return True/False
        users_with_email = self.filter(email=email)
        if not users_with_email:
            return False
        user = users_with_email[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def validate(self, form_data):
        
        errors = {}
        if len(form_data['first_name']) < 1:
            errors['first_name'] = 'First Name field is required.'

        if len(form_data['last_name']) < 1:
            errors['last_name'] = 'Last Name field is required.'

        if len(form_data['email']) < 5:
            errors['email'] = 'email must be at least 5 characters.'


        if form_data['password'] != form_data['confirm']:
            errors['password'] = "Passwords do not match"
        
        
        users_with_email = self.filter(email=form_data['email']) #checks if email is taken
        if users_with_email: # if NON-EMPTY list
            errors['email'] = 'email already in use.'

        return errors

  

class User(models.Model):
    
    avatar = models.ImageField(upload_to = 'images/', null = True, blank = True) #change to another pic
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} Profile'

