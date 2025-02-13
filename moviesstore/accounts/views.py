from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import CustomPasswordResetForm

# Create your views here.

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

#def resetpassword(request):
    #template_data = {}
    #template_data['title'] = 'ResetPassword'
    #if request.method == 'GET':
        #return render(request, 'accounts/resetpassword.html',
           # {'template_data': template_data})
    #if request.method == 'POST':
    #    form = PasswordResetForm(request.POST)

@login_required
def resetpassword(request):
    template_data = {'title': 'Reset Password'}

    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(username=username)

            # Set new password
            user.set_password(new_password)
            user.save()

            # Keep user logged in after password reset
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been successfully updated.")
            return redirect('home.index')  # Redirect to profile or another relevant page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomPasswordResetForm()

    template_data['form'] = form
    return render(request, 'accounts/resetpassword.html', template_data)

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
                      {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class = CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                          {'template_data': template_data})

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
        {'template_data': template_data})