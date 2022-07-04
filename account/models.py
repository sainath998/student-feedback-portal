from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    User,
)
# from django.contrib.postgres.fields import ArrayField

from personal.models import (
    DESIGNATION,
    SEMESTER,

    Department,
    Course,
)

# Create your models here.

class Validation(models.Model) :
    otp = models.IntegerField(null=False)


class Student(models.Model) :
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=50, null=False)
    enrollment_no = models.CharField(max_length=15, null=False)
    email_id = models.EmailField(max_length=50, null=False)
    anonymous_id = models.CharField(max_length=50, null=False, unique=True)


    semester = models.CharField(max_length=50, null=True, choices=SEMESTER)

    submitted_feedbacks = models.ManyToManyField(Course, blank=True)
    # submitted_feedbacks = []
    # submitted_feedbacks = ArrayField(models.CharField(max_length=256), default=list)

    def __str__(self) :
        return str(self.name)


class Faculty(models.Model) :
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, unique=True)
    # username = models.CharField(max_length=255, unique=True)


    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    designation = models.CharField(max_length=255, null=True, choices=DESIGNATION)

    def __str__(self) :
        return str(self.designation) + '. ' + str(self.name)