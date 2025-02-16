from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django import forms
from .models import CustomUser
from django.utils.safestring import mark_safe


SECURITY_QUESTIONS = [
    ("birth_city", "What city were you born in?"),
    ("first_pet", "What was the name of your first pet?"),
    ("mother_maiden", "What is your mother’s maiden name?"),
    ("favorite_teacher", "Who was your favorite teacher in school?"),
]


class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([
            f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))

class CustomUserCreationForm(UserCreationForm):
    security_question_1 = forms.ChoiceField(
        choices=SECURITY_QUESTIONS,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Security Question 1"
    )
    security_answer_1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Answer 1"
    )
    security_question_2 = forms.ChoiceField(
        choices=SECURITY_QUESTIONS,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Security Question 2"
    )
    security_answer_2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Answer 2"
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'password1','password2', 'security_question_1', 'security_answer_1', 'security_question_2', 'security_answer_2')
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update(
                {'class': 'form-control'}
            )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # password1 = self.cleaned_data['password1']
        # user.set_password(password1)
        user.securityQ1 = self.cleaned_data['security_question_1']
        user.securityA1 = self.cleaned_data['security_answer_1']
        user.securityQ2 = self.cleaned_data['security_question_2']
        user.securityA2 = self.cleaned_data['security_answer_2']
        if commit:
            user.save()
        # custom_user = CustomUser.objects.create(user=user, securityQ1=securityQ1, securityA1=securityA1, securityQ2=securityQ2, securityA2=securityA2)
            
        return user
    
class ResetPasswordForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Username"
    )
    security_question_1 = forms.ChoiceField(
        choices=SECURITY_QUESTIONS,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Security Question 1"
    )
    security_answer_1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Answer 1"
    )
    security_question_2 = forms.ChoiceField(
        choices=SECURITY_QUESTIONS,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Security Question 2"
    )
    security_answer_2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Answer 2"
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="New Password"
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm New Password"
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        if new_password and confirm_new_password and new_password != confirm_new_password:
            raise forms.ValidationError("New passwords do not match.")
        return cleaned_data
