from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST


# Create your views here.
@login_required()
#if user has successfully authenticated run this
def dashboard(request):
    return render(request, 'account/dashboard.html')
def about(request):
    return render(request, 'account/about.html')
def logged_out(request):
    return render(request, 'account/logged_out.html')



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request, username=cd['username'],
                                       password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Your account has been deactivated')


        else:
            messages.error(request, 'Invalid login')
    else:
        form=LoginForm()
    if request.method == 'POST':
        user_form=UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user=user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            login(request, new_user)
            messages.success(request, 'Account created')
            return redirect('dashboard')
    else:
        user_form=UserRegistrationForm()


    return render(request, 'account/login.html', {'form':form,
        'user_form':user_form})


def register(request):
    if request.method == 'POST':
        user_form=UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user=user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html',
                    {'new_user':new_user})
    else:
        user_form=UserRegistrationForm()

    return render(request, 'account/register.html',{'user_form':user_form})


def edit(request):
    if request.method == 'POST':
        user_form=UserEditForm(instance=request.user, data=request.POST)
        profile_form=ProfileEditForm(instance=request.user.profile,
                data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating  your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',
            {'user_form':user_form,
                'profile_form':profile_form})


