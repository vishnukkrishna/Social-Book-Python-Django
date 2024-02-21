from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout, login as auth_login
from django.contrib import messages
from .models import *
from django.http import HttpResponse

# Create your views here.

def index(request):
  return render(request, 'index.html')


def signup(request):

  if request.method == 'POST':
    username  = request.POST['username']
    email     = request.POST['email']
    password  = request.POST['password']
    password2 = request.POST['password2']

    if password == password2:
      if User.objects.filter(email=email).exists():
        messages.info(request, "Email Taken")
        return redirect('signup')
      elif User.objects.filter(username=username).exists():
        messages.info(request, "Username Taken")
        return redirect('signup')
      else:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Log user in and redirect to settings page

        # Create a Profile object for the new user
        user_model  = User.objects.get(username=username)
        new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
        new_profile.save()
        return redirect('signup')
    else:
      messages.info(request, "Password Not Matching")
      return redirect('signup')
  else:
    return render(request, 'signup.html')
  

def signin(request):

  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if user is not None:
      auth_login(request, user)
      return redirect('/')
    else:
      messages.info(request, "Credentials Invalid")
      return redirect('signin')
  else:
    return render(request, 'signin.html')
  


