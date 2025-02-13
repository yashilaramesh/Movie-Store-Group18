from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([
            f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))
class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1',
        'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update(
                {'class': 'form-control'}
            )

class CustomPasswordResetForm(forms.Form):
    username = forms.CharField(label="Username", max_length=150)
    new_password = forms.CharField(label="Enter New Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        # Check if passwords match
        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        # Check if user exists
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username does not exist.")

        return cleaned_data