from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib.auth.hashers import make_password

# Create your views here.

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def resetpassword(request):
    template_data = {}
    template_data['title'] = 'ResetPassword'
    if request.method == 'GET':
        return render(request, 'accounts/resetpassword.html',
            {'template_data': template_data})
    #if request.method == 'POST':
    #    form = PasswordResetForm(request.POST)

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
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class = CustomErrorList)
        if form.is_valid():

            user = form.save(commit=False)
            # user.password = make_password(form.cleaned_data['password1'])
            user.save()

           # user.securityQ1 = form.cleaned_data['securityQ1']
            #user.securityQ2 = form.cleaned_data['securityQ2']
            #user.securityA1 = form.cleaned_data['securityA1']
           # user.securityA2 = form.cleaned_data['securityA1']
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
        {'template_data': template_data})