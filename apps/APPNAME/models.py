# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re, datetime, bcrypt

# Create your models here.
class UserManager(models.Manager):
    def register(self, data):
        errors = []
        if len(data['first_name'])<2:
            errors.append("First name must consist 3 or more characters.")
        if not data['first_name'].isalpha():
            errors.append("First name must be only letters.")
        if len(data['last_name'])<2:
            errors.append("Last name must consist 3 or more characters.")
        if not data['last_name'].isalpha():
            errors.append("Last name must be only letters.")
        if data['username']=="":
            errors.append("Username may not be blank.")
        try:
            User.objects.get(username=data['username'])
            errors.append("Entered username already exists.")
        except:
            pass
        if len(data['password'])<8:
            errors.append("Password must be at least 8 characters long")
        if data['password']!=data['confirm_password']:
            errors.append("Password and Confirm Password don't match.")

        if len(errors)>0:
            return{
            'new':None,
            'errors_list':errors,
            }
        else:
            data['password']=bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            new_user=User.objects.create(first_name=data['first_name'], last_name=data['last_name'], username=data['username'], password=data['password'])
            return{
            'new':new_user,
            'errors_list':None,
            }

    def login(self, data):
        errors = []
        try:
            found_user = User.objects.get(username=data['username'])
            if bcrypt.hashpw(data['password'].encode('utf-8'), found_user.password.encode('utf-8')) != found_user.password.encode('utf-8'):
                errors.append("Incorrect password.")
        except:
            errors.append("Entered username does not exist. (username is case sensitive)")

        if len(errors)>0:
            return{
            'logged_user':None,
            'errors_list':errors,
            }
        else:
            return{
            'logged_user':found_user,
            'errors_list':None,
            }

class TravelManager(models.Manager):
    def add(self, data):
        errors = []
        if data['travel_destination']=='':
            errors.append("Destination may not be empty")
        if data['travel_description']=='':
            errors.append("Description may not be empty")
        if data['travel_date_from']=='':
            errors.append("Travel Date From may not be empty")
        elif datetime.datetime.strptime(data['travel_date_from'], '%Y-%m-%d') <= datetime.datetime.now():
            errors.append("Travel Date From must be in future.")
        if data['travel_date_to']=='':
            errors.append("Travel Date To may not be empty")
        elif datetime.datetime.strptime(data['travel_date_to'], '%Y-%m-%d') < datetime.datetime.strptime(data['travel_date_from'], '%Y-%m-%d'):
            errors.append("Relationship with Travel Date From & Travel Date To does not make sense.")

        if len(errors)>0:
            return{
            'new':None,
            'errors_list':errors,
            }
        else:
            new_plan=Travel.objects.create(travel_destination=data['travel_destination'], travel_description=data['travel_description'],travel_start_date=data['travel_date_from'],travel_end_date=data['travel_date_to'],user=User.objects.get(id=data['travel_user_id']))
            return{
            'new':new_plan,
            'errors_list':None,
            }


class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

class Travel(models.Model):
    travel_destination=models.CharField(max_length=255)
    travel_description=models.CharField(max_length=255)
    travel_start_date=models.CharField(max_length=255)
    travel_end_date=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=TravelManager()
    user=models.ForeignKey(User)

class Join(models.Model):
    user=models.ForeignKey(User)
    travel=models.ForeignKey(Travel)
