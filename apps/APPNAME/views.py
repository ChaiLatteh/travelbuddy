# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, UserManager, Travel, TravelManager, Join
import datetime

# Create your views here.
def index(request):
    return render(request, 'APPNAME/index.html')

def register(request):
    context = {
    'first_name':request.POST['reg_first_name'],
    'last_name':request.POST['reg_last_name'],
    'username':request.POST['reg_username'],
    'password':request.POST['reg_password'],
    'confirm_password':request.POST['reg_confirm_password'],
    }
    new_user = User.objects.register(context)

    if new_user['errors_list']:
        for error in new_user['errors_list']:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')
    else:
        messages.add_message(request, messages.ERROR, "Successfully Registered!")
        return redirect('/')

def login(request):
    context = {
    'username':request.POST['login_username'],
    'password':request.POST['login_password'],
    }
    user = User.objects.login(context)
    if user['errors_list']:
        for error in user['errors_list']:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')
    else:
        request.session['user_id']=user['logged_user'].id
        request.session['first_name']=user['logged_user'].first_name
        request.session['last_name']=user['logged_user'].last_name
        return redirect('/travels')

def travels(request):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, "You must be logged in to view this page.")
        return redirect('/')

    # if today is the date after travel's start date, delete that travel.
    for travel in Travel.objects.all():
        if datetime.datetime.strptime(travel.travel_start_date, '%Y-%m-%d') < datetime.datetime.now():
            travel.delete()


    current_user=User.objects.get(id=request.session['user_id'])
    my_travels_list=[]
    others_travels_list=[]

    for travel in Travel.objects.all():
        if travel.user.id==request.session['user_id']:
            my_travels_list.append(travel)
        else:
            try:
                # try looking for Join object with this user and this travel. if found, it means that user clicked Join, so append it to my_travels_list
                Join.objects.get(user=current_user, travel=travel)
                my_travels_list.append(travel)
            except:
                # if Join object with this user and this travel not found, user did not click Join, so move it to others_travels_list
                others_travels_list.append(travel)

    context = {
    "my_travels_list":my_travels_list,
    "others_travels_list":others_travels_list,
    }

    return render(request, 'APPNAME/travels.html', context)

def travels_add(request):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, "You must be logged in to view this page.")
        return redirect('/')
    return render(request, 'APPNAME/travels_add.html')

def travels_add_process(request):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, "You must be logged in to view this page.")
        return redirect('/')

    context = {
    'travel_destination':request.POST['travel_destination'],
    'travel_description':request.POST['travel_description'],
    'travel_date_from':request.POST['travel_date_from'],
    'travel_date_to':request.POST['travel_date_to'],
    'travel_user_id':request.session['user_id'],
    }
    new_plan=Travel.objects.add(context)
    if new_plan['errors_list']:
        for error in new_plan['errors_list']:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/travels/add')
    else:
        request.session['recent_add']=new_plan['new'].id
        print request.session['recent_add']
        messages.add_message(request, messages.ERROR, "Successfully planned!")
        return redirect('/travels')

def travel_join(request, travel_id):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, "You must be logged in to view this page.")
        return redirect('/')

    this_user=User.objects.get(id=request.session['user_id'])
    this_travel=Travel.objects.get(id=travel_id)
    try:
        Join.objects.get(travel=this_travel,user=this_user)
        messages.add_message(request, messages.ERROR, "INVALID APPROACH")
        return redirect('/travels')
    except:
        Join.objects.create(travel=this_travel, user=this_user)

    messages.add_message(request, messages.ERROR, "Successfully Joined!")
    return redirect('/travels')

def travel_unjoin(request, travel_id):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, "You must e logged in to view this page.")
        return redirect('/')

    this_user=User.objects.get(id=request.session['user_id'])
    this_travel=Travel.objects.get(id=travel_id)
    try:
        Join.objects.get(travel=this_travel, user=this_user).delete()
    except:
        messages.add_message(request, messages.ERROR, "INVALID APPROACH")
        return redirect('/travels')

    messages.add_message(request, messages.ERROR, "You have successfully bailed on the plan!")
    return redirect('/travels')


def travel_view(request, travel_id):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, "You must be logged in to view this page.")
        return redirect('/')
    this_travel=Travel.objects.get(id=travel_id)
    joined_users_list=[]
    try:
        for joined_user in this_travel.join_set.all():
            joined_users_list.append(joined_user.user)
    except:
        pass
    join_list = Join.objects.all()
    #Join with travel=Travel.objects.get(id=travel_id) and user=this_travel.user

    context = {
    "this_travel":this_travel,
    "joined_users_list":joined_users_list,
    "join_list":join_list,
    }
    return render(request, 'APPNAME/travel_view.html', context)

def updates(request):
    return render(request, 'APPNAME/updates.html')

def logout(request):
    request.session.clear()
    return redirect('/')
