from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout as auth_logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.urls import reverse
from django.http import HttpResponse

# Create your views here.

@login_required(login_url='signin')
def index(request):
  return render(request, 'index.html')


@login_required(login_url='signin')
def settings(request):
  try:
    user_profile = Profile.objects.get(user=request.user)
  except Profile.DoesNotExist:
    user_profile = Profile.objects.create(user=request.user, id_user=request.user.id)
      
  if request.method == 'POST':
    if request.FILES.get('image') == None:
        image     = user_profile.profileimg
        bio       = request.POST['bio']
        location  = request.POST['location']
        user_profile.bio      = bio
        user_profile.location = location
        user_profile.save()
    else:
        image    = request.FILES.get('image')
        bio      = request.POST['bio']
        location = request.POST['location']
        user_profile.profileimg = image
        user_profile.bio        = bio
        user_profile.location   = location
        user_profile.save()

    return redirect(reverse('settings'))

  return render(request, 'setting.html', {'user_profile': user_profile})



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
        user_login = authenticate(username=username, password=password)
        auth_login(request, user_login)

        # Create a Profile object for the new user
        user_model  = User.objects.get(username=username)
        new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
        new_profile.save()
        return redirect('settings')
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
  

@login_required(login_url='signin')
def logout(request):
  auth_logout(request)
  return redirect('signin')