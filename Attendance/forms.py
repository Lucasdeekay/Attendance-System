from django import forms


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
    full_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Full Name',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    staff_id = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Staff ID',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    email = forms.EmailField(
        max_length=30,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email Address',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    gender = forms.CharField(
        max_length=30,
        widget=forms.Select(
            choices=[
                ('', 'Select Gender...'),
                ('MALE', 'MALE'),
                ('FEMALE', 'FEMALE'),
            ],
            attrs={
                'required': '',
                'class': 'form-control',
            }
        )
    )
    department = forms.CharField(
        max_length=30,
        widget=forms.Select(
            choices=[
                ('', 'Select Department...'),
                ('COMPUTER SCIENCES', 'COMPUTER SCIENCES'),
                ('BIOLOGICAL SCIENCES', 'BIOLOGICAL SCIENCES'),
                ('CHEMICAL SCIENCES', 'CHEMICAL SCIENCES'),
                ('MANAGEMENT SCIENCES', 'MANAGEMENT SCIENCES'),
                ('MASS COMMUNICATION', 'MASS COMMUNICATION'),
                ('CRIMINOLOGY', 'CRIMINOLOGY'),
                ('GENERAL STUDIES', 'GENERAL STUDIES'),
            ],
            attrs={
                'required': '',
                'class': 'form-control',
            }
        )
    )

    def clean(self):
        cleaned_data = super(StaffRegisterForm, self).clean()
        full_name = cleaned_data.get('full_name')
        staff_id = cleaned_data.get('staff_id')
        email = cleaned_data.get('email')
        gender = cleaned_data.get('gender')
        department = cleaned_data.get('department')
        if not full_name or not staff_id or not email or not gender or not department:
            raise forms.ValidationError("Field cannot be empty")


class StudentRegisterForm(forms.Form):
    full_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Full Name',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    matric_no = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Matric No',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    email = forms.EmailField(
        max_length=30,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email Address',
                'class': 'form-control',
            }
        )
    )
    gender = forms.CharField(
        max_length=30,
        widget=forms.Select(
            choices=[
                ('', 'Select Gender...'),
                ('Male', 'Male'),
                ('Female', 'Female'),
            ],
            attrs={
                'required': '',
                'class': 'form-control',
            }
        )
    )
    programme = forms.CharField(
        max_length=30,
        widget=forms.Select(
            choices=[
                ('', 'Select Programme...'),
                ('CYBER SECURITY', 'CYBER SECURITY'),
                ('COMPUTER SCIENCE', 'COMPUTER SCIENCE'),
                ('SOFTWARE ENGINEERING', 'SOFTWARE ENGINEERING'),
                ('MICROBIOLOGY', 'MICROBIOLOGY'),
                ('INDUSTRIAL CHEMISTRY', 'INDUSTRIAL CHEMISTRY'),
                ('BIOCHEMISTRY', 'BIOCHEMISTRY'),
                ('BUSINESS ADMINISTRATION', 'BUSINESS ADMINISTRATION'),
                ('ECONOMICS', 'ECONOMICS'),
                ('ACCOUNTING', 'ACCOUNTING'),
                ('MASS COMMUNICATION', 'MASS COMMUNICATION'),
                ('CRIMINOLOGY', 'CRIMINOLOGY'),
            ],
            attrs={
                'required': '',
                'class': 'form-control',
            }
        )
    )
    year_of_entry = forms.CharField(
        max_length=30,
        widget=forms.Select(
            choices=[
                ('', 'Select Session...'),
                ('2022/2023', '2022/2023'),
                ('2023/2024', '2023/2024'),
                ('2024/2025', '2024/2025'),
                ('2025/2026', '2025/2026'),
                ('2026/2027', '2026/2027'),
                ('2027/2028', '2027/2028'),
                ('2028/2029', '2028/2029'),
                ('2029/2030', '2029/2030'),
            ],
            attrs={
                'required': '',
                'class': 'form-control',
            }
        )
    )

    def clean(self):
        cleaned_data = super(StudentRegisterForm, self).clean()
        full_name = cleaned_data.get('full_name')
        matric_no = cleaned_data.get('matric_no')
        email = cleaned_data.get('email')
        gender = cleaned_data.get('gender')
        programme = cleaned_data.get('programme')
        year_of_entry = cleaned_data.get('year_of_entry')
        if not full_name or not matric_no or not email or not gender or not programme or not year_of_entry:
            raise forms.ValidationError("Field cannot be empty")


class ForgotPasswordForm(forms.Form):
    user_id = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter Matric No/Staff Username',
                'required': '',
                'class': 'input',
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter Email',
                'required': '',
                'class': 'input',
            }
        )
    )

    def clean(self):
        cleaned_data = super(ForgotPasswordForm, self).clean()
        user_id = cleaned_data.get('user_id')
        email = cleaned_data.get('email')
        if not user_id or not email:
            raise forms.ValidationError("Field cannot be empty")


class PasswordRetrievalForm(forms.Form):
    password = forms.CharField(
        max_length=12,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter Password',
                'required': '',
                'class': 'input',
            }
        )
    )

    def clean(self):
        cleaned_data = super(PasswordRetrievalForm, self).clean()
        password = cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("Field cannot be empty")


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter Password',
                'required': '',
                'class': 'input',
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm Password',
                'required': '',
                'class': 'input',
            }
        )
    )

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if not password or not confirm_password:
            raise forms.ValidationError("Field cannot be empty")


class UpdatePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter Old Password',
                'required': '',
                'class': 'input',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter New Password',
                'required': '',
                'class': 'input',
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm New Password',
                'required': '',
                'class': 'input',
            }
        )
    )

    def clean(self):
        cleaned_data = super(UpdatePasswordForm, self).clean()
        old_password = cleaned_data.get('old_password')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if not old_password or not password or not confirm_password:
            raise forms.ValidationError("Field cannot be empty")


class UpdateEmailForm(forms.Form):
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email Address',
                'class': 'form-control',
                'required': '',
            }
        )
    )

    def clean(self):
        cleaned_data = super(UpdateEmailForm, self).clean()
        email = cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Field cannot be empty")


class UploadImageForm(forms.Form):
    image = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'required': '',
                'class': 'input',
            }
        )
    )

    def clean(self):
        cleaned_data = super(UploadImageForm, self).clean()
        image = cleaned_data.get('image')
        if not image:
            raise forms.ValidationError("Field cannot be empty")


class UploadFileForm(forms.Form):
    session = forms.CharField(
        max_length=30,
        widget=forms.Select(
            choices=[
                ('', 'Select Session...'),
                ('2022/2023', '2022/2023'),
                ('2023/2024', '2023/2024'),
                ('2024/2025', '2024/2025'),
                ('2025/2026', '2025/2026'),
                ('2026/2027', '2026/2027'),
                ('2027/2028', '2027/2028'),
                ('2028/2029', '2028/2029'),
                ('2029/2030', '2029/2030'),
            ],
            attrs={
                'required': '',
                'class': 'form-control',
            }
        )
    )
    file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'required': '',
                'class': 'input',
            }
        )
    )

    def clean(self):
        cleaned_data = super(UploadFileForm, self).clean()
        session = cleaned_data.get('session')
        file = cleaned_data.get('file')
        if not file or not session:
            raise forms.ValidationError("Field cannot be empty")

