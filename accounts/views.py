from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from .forms import UserForm
from vendor.forms import vendorForm
from .models import User, UserProfile
from vendor.models import Vendor
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from .utils import check_role_customer, check_role_vendor, send_verification_mail
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

# Create your views here.


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already loggedin!')
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            # ready to save but not saved into database
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()
            mail_subject = 'Verify your mail'
            mail_template = 'accounts/mail/account_verification_mail.html'

            send_verification_mail(request, user, mail_template, mail_subject)
            messages.success(
                request, 'Congratulations! Your account has been successfully registered. Check your mail to activate your account')
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
            mail_subject = 'Verify your mail'
            mail_template = 'accounts/mail/account_verification_mail.html'
            send_verification_mail(request, user, mail_template, mail_subject)
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


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'You are account successfully activated.')
        return redirect('myaccount')
    else:
        messages.error(request, 'invalid activation link')
        return redirect('myaccount')


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are alreay loggedin!')
        return redirect('dashboard')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
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


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            mail_subject = 'Password reset'
            mail_template = 'accounts/mail/password_reset_confirm_mail.html'
            send_verification_mail(request, user, mail_template, mail_subject)
            messages.info(request, 'Please check your mail!')
        else:
            messages.error(request, 'mail does not exist')
    return render(request, 'accounts/forgot_password.html')


def password_reset(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        print(uid)
        # uid=urlsafe_base64_decode(uuidb64).decode
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        return redirect('password_reset_done')


def password_reset_done(request):
    if request.method == 'POST':
        password = request.POST['password']
        password1 = request.POST['confirm_password']
        if password == password1:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password successfully reset')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('password_reset_done')

    return render(request, 'accounts/password_reset_done.html')
