from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .forms import ResetPasswordForm

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


def resetpassword(request):
    template_data = {'title': 'Reset Password'}
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            security_question_1 = form.cleaned_data['security_question_1']
            security_answer_1 = form.cleaned_data['security_answer_1']
            security_question_2 = form.cleaned_data['security_question_2']
            security_answer_2 = form.cleaned_data['security_answer_2']
            new_password = form.cleaned_data['new_password']

            User = get_user_model()
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                template_data['error'] = "Username not found."
                return render(request, 'accounts/resetpassword.html', {'template_data': template_data, 'form': form})

            if (
                user.securityQ1 == security_question_1 and user.securityA1.lower() == security_answer_1.lower()
                and user.securityQ2 == security_question_2 and user.securityA2.lower() == security_answer_2.lower()
            ):
                user.set_password(new_password)
                user.save()
                return redirect('accounts.login')
            else:
                template_data['error'] = "Incorrect security question answers."
    
    else:
        form = ResetPasswordForm()

    template_data['form'] = form
    return render(request, 'accounts/resetpassword.html', {'template_data': template_data})