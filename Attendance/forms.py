from django import forms

from Attendance.models import Department, Course


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your username',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter your password',
                'required': '',
                'class': 'form-control',
            }
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not username or not password:
            raise forms.ValidationError("Field cannot be empty")


class UpdatePasswordForm(forms.Form):
    password = forms.CharField(
        help_text="Minimum of 8 characters",
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'required': '',
                'class': 'form-control form-control-sm rounded bright',
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm password',
                'required': '',
                'class': 'form-control form-control-sm rounded bright',
            }
        )
    )

    def clean(self):
        cleaned_data = super(UpdatePasswordForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if not password or not confirm_password:
            raise forms.ValidationError("Field cannot be empty")


