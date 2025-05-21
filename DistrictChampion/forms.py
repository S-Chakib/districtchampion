from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            #'class': 'form-control form-control-sm custom-input',
            'class': 'custom-input',
            'placeholder': 'Username',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'custom-input',
            'placeholder': 'Password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'custom-input',
            'placeholder': 'Confirm password',
        })

    # Remove help texts
        for field in self.fields.values():
            field.help_text = ''


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'custom-input',
            'placeholder': 'Username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'custom-input',
            'placeholder': 'Password',
        })

        # Optional: remove help texts
        for field in ['username', 'password']:
            self.base_fields[field].help_text = ''




'''

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'custom-input',
                #'style': 'background-color: black; color: orange;',
            })


'''
