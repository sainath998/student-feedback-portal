from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . models import (
    Validation,
    Faculty,
    Student,
)

class UserRegistrationForm(UserCreationForm) :
    enrollment_no = forms.CharField(max_length=15)
    # email = forms.EmailField()
    # first_name = forms.CharField(max_length=50)
    # last_name = forms.CharField(max_length=50)

    class Meta :
        model = User
        fields = ('enrollment_no', 'username', 'password1', 'password2')


class FacultyRegistrationForm(UserCreationForm) :
    # name = forms.CharField(max_length=255)
    # email = forms.EmailField(max_length=255)

    class Meta :
        model = User
        fields = ('email', 'password1', 'password2')


class StudentProfileForm(forms.ModelForm) :
    class Meta :
        model = User
        fields = ('username',)

    def clean_username(self) :
        if self.is_valid() :
            username = self.cleaned_data['username']
            try :
                user = User.objects.exclude(pk = self.instance.pk).get(username=username)
            except :
                return username

            raise forms.ValidationError(f'username {user.username} is already in use...')



# difference between StudentProfileForm and FacultyProfileForm,
    # in student form I am using the model = User and only allowing to change the username
    # in faculty form I am using the model = Faculty and only allowing to change the
class FacultyProfileForm(forms.ModelForm) :
    class Meta :
        model = Faculty
        fields = ('name',)

class VerificationForm(ModelForm) :
    # otp = forms.IntegerField(max_value=999999, min_value=100000)

    class Meta :
        model = Validation
        fields = ('otp',)