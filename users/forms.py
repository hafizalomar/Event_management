from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from event.forms import StyledFormMixin

class RegisterForm(StyledFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.apply_styled_widgets()

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None