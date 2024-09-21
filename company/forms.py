from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="A valid email address is required.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class UploadFileForm(forms.Form):
    file = forms.FileField()
