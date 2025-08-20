import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from event.forms import StyledFormMixin
from users.models import Profile

class RegisterForm(StyledFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.apply_styled_widgets()

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class CustomRegistrationForm(StyledFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    phone_number = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # keep only real User fields

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        print(phone_number)

        # check only digits allowed (10–15 digits)
        if not re.fullmatch(r'^\+?\d{10,15}$', phone_number):
            raise forms.ValidationError("Enter a valid phone number (10–15 digits, optional +).")

        # check uniqueness
        if Profile.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Phone number already exists")

        return phone_number

    def clean_password(self):
        password = self.cleaned_data.get('password')
        errors = []

        if len(password) < 8:
            errors.append('Password must be at least 8 characters long.')

        if not re.search(r'[A-Z]', password):
            errors.append('Password must include at least one uppercase letter.')

        if not re.search(r'[a-z]', password):
            errors.append('Password must include at least one lowercase letter.')

        if not re.search(r'[0-9]', password):
            errors.append('Password must include at least one number.')

        if not re.search(r'[@#$&]', password):
            errors.append('Password must include at least one special character (@, #, $, &).')

        if errors:
            raise forms.ValidationError(errors)

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data