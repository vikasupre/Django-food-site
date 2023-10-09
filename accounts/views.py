from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from .forms import UserForm
from vendor.forms import vendorForm
from .models import User, UserProfile
from vendor.models import Vendor
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.urls import resolve


# Create your views here.


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already loggedin!')
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            print(password)
            # ready to save but not saved into database
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(
                request, 'Congratulations! Your account has been successfully registered.')
            return redirect('registerUser')
        else:
            messages.error(
                request, 'Registration Failed: Please check the following and try again:')

    else:
        form = UserForm()
    context = {'form': form}
    return render(request, 'accounts/registerUser.html', context)


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already loggedin!')
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        v_form = vendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.role = User.VENDOR
            user.set_password(password)
            user.save()
            # vendr profile details
            vendor = v_form.save(commit=False)
            vendor.user = user
            userprofile = UserProfile.objects.get(user=user)
            vendor.user_profile = userprofile
            vendor.save()
            messages.success(
                request, 'You account has been successfully registered.Please wiat for the approval.')
        else:
            messages.error(
                request, 'Registration Failed: Please check the following and try again:')
    else:
        form = UserForm()
        v_form = vendorForm()
    context = {'v_form': v_form, 'form': form}
    return render(request, 'accounts/registerVendor.html', context)


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are alreay loggedin!')
        return redirect('dashboard')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(password)
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are successfully loggedin!')
            return redirect('dashboard')
        else:
            messages.error(request, 'invalid login credentials')
    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'You have successfully logged out!')
    return redirect('login')


def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


@login_required()
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


@login_required()
def MyAccount(request):
    if request.user.role == 1:
        return redirect('vendorMyAccount')
    elif request.user.role == 2:
        return redirect('customerMyAccount')
    elif request.user.role == None:
        return redirect('admin')


@login_required()
@user_passes_test(check_role_customer)
def customerMyAccount(request):
    return render(request, 'accounts/customerMyAccount.html')


@login_required()
@user_passes_test(check_role_vendor)
def vendorMyAccount(request):
    return render(request, 'accounts/vendorMyAccount.html')
