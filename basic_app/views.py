from django.shortcuts import render
from basic_app.forms import Userform, UserProfileForm
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django import forms

# Create your views here.
def index(request, registered=False, comments=''):
    return render(request, 'html/index.html', context={'registered':registered, 'comments':comments})

def register_page(request):
    user_form = Userform()
    profile_form = UserProfileForm()
    if request.method == "POST":
        user_form = Userform(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            return index(request, True)
        else:
            print(user_form.errors, profile_form.errors)

    return render(request, 'html/register.html', context={'user_form':user_form, 
                                                            'profile_form':profile_form,})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account not active')
        else:
            print('Someone tried to login and failed')
            print('username: {} and password: {}'.format(username, password))
            return index(request, False, 'Invalid login details supplied \n Please try to login again')
    else:
        return render(request, 'html/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def user_special(request):
    return HttpResponse('You are logged in. Nice!')