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


class StaffRegisterForm(forms.Form):
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your last name',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your first name',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    middle_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your middle name',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    staff_id = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your staff id',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    post = forms.CharField(
        max_length=30,
        widget=forms.Select(
            choices=[
                ('Lecturer I', 'Lecturer I'),
                ('Lecturer II', 'Lecturer II'),
            ],
            attrs={
                'placeholder': 'Enter your post',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    department = forms.CharField(
        max_length=30,
        widget=forms.Select(
            choices=[
                ('Computer Science', 'Computer Science'),
                ('Biological Science', 'Biological Science'),
                ('Chemical Science', 'Chemical Science'),
                ('Business Administration', 'Business Administration'),
                ('Mass Communication', 'Mass Communication'),
                ('Criminology', 'Criminology'),
                ('Accounting', 'Accounting'),
            ],
            attrs={
                'placeholder': 'Enter your department',
                'required': '',
                'class': 'form-control',
            }
        )
    )

    def clean(self):
        cleaned_data = super(StaffRegisterForm, self).clean()
        last_name = cleaned_data.get('last_name')
        first_name = cleaned_data.get('first_name')
        middle_name = cleaned_data.get('middle_name')
        staff_id = cleaned_data.get('staff_id')
        post = cleaned_data.get('post')
        department = cleaned_data.get('last_name')
        if not last_name or not first_name or not middle_name or not staff_id or not post or not department:
            raise forms.ValidationError("Field cannot be empty")


class StudentRegisterForm(forms.Form):
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your last name',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your first name',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    middle_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your middle name',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    matric_no = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your matric no',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    programme = forms.CharField(
        max_length=30,
        widget=forms.Select(
            choices=[
                ('Computer Science', 'Computer Science'),
                ('Software Engineering', 'Software Engineering'),
                ('Cyber Security', 'Cyber Security'),
                ('Biochemistry', 'Biochemistry'),
                ('Industrial Chemistry', 'Industrial Chemistry'),
                ('Business Administration', 'Business Administration'),
                ('Mass Communication', 'Mass Communication'),
                ('Criminology', 'Criminology'),
                ('Microbiology', 'Microbiology'),
                ('Economics', 'Economics'),
                ('Accounting', 'Accounting'),
            ],
            attrs={
                'placeholder': 'Enter your programme',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    level = forms.CharField(
        max_length=30,
        widget=forms.Select(
            choices=[
                ('100', '100'),
                ('200', '200'),
                ('300', '300'),
                ('400', '400'),
            ],
            attrs={
                'placeholder': 'Enter your level',
                'required': '',
                'class': 'form-control',
            }
        )
    )

    def clean(self):
        cleaned_data = super(StaffRegisterForm, self).clean()
        last_name = cleaned_data.get('last_name')
        first_name = cleaned_data.get('first_name')
        middle_name = cleaned_data.get('middle_name')
        matric_no = cleaned_data.get('matric_no')
        level = cleaned_data.get('level')
        programme = cleaned_data.get('programme')
        if not last_name or not first_name or not middle_name or not matric_no or not level or not programme:
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


