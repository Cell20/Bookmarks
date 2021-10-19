from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib import messages


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        messages.error(request, 'Error updating your profile')

    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'account/edit.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated Successfully')
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'account/login.html', context)


@login_required
def dashboard(request):
    context = {'section': 'dashboard'}
    return render(request, 'account/dashboard.html', context)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            # Instead of saving raw pwd we use set method to save hashed pwd
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            messages.success(request, 'Account created successfully')
            context = {'new_user': new_user}
            return render(request, 'account/register_done.html', context)
        else:
            messages.warning(request, 'Please fill the fields correctly')

    else:
        user_form = UserRegistrationForm()

    context = {'user_form': user_form}
    return render(request, 'account/register.html', context)
