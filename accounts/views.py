from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from .forms import UserRegistrationForm
from .models import User
from django.contrib import messages

# Create your views here.


def registerUser(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
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
            print('invalid form')
            print(form.errors)
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'accounts/registerUser.html', context)
