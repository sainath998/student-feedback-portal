from django import forms
from django.forms import ModelForm


from .models import (
    Course,
    Department,
)

from account.models import (
    Faculty,
)

class CourseForm(ModelForm) :
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label='Department')

    class Meta :
        model = Course
        fields = '__all__'