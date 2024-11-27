from django import forms
from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import ValidationError
from employees.models import Employee, EmployeeJob, EmployeeJobLevel, EmployeeJobSpecialty, EmployeeStatus
from employees.utils import generate_username


class EmployeeCreationForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    gender = forms.ChoiceField(
        choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')])
    email = forms.EmailField(required=True)

    class Meta:
        model = Employee
        fields = [
            'company_id',
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'gender',
            'contact',
            'birth_date',
            'address',
            'status',
            'start_date',
            'position',
            'position_level',
            'position_specialties',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].initial = 'welcome01'
        self.fields['password2'].initial = 'welcome01'
        self.fields['password1'].widget.attrs['value'] = 'welcome01'
        self.fields['password2'].widget.attrs['value'] = 'welcome01'
        self.fields['password1'].widget = forms.HiddenInput()
        self.fields['password2'].widget = forms.HiddenInput()

    def clean_password1(self):
        return 'welcome01'

    def clean_password2(self):
        return 'welcome01'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        start_date = cleaned_data.get('start_date')
        regular_date = cleaned_data.get('regular_date')

        if (password1 and password2) and (password1 != password2):
            raise forms.ValidationError("Passwords do not match.")
        if not start_date:
            raise ValidationError({'start_date': 'Start date is required.'})
        if (regular_date and start_date) and (regular_date < start_date):
            raise ValidationError(
                {'regular_date': 'Regular date cannot be earlier than start date.'})

        return cleaned_data

    def clean_company_id(self):
        return self.cleaned_data['company_id'].upper()

    def save(self, commit=True):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        username = generate_username(first_name)
        email = self.cleaned_data.get('email')

        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        employee = super().save(commit=False)
        employee.user = user

        if commit:
            employee.save()
            self.save_m2m()

        return employee
