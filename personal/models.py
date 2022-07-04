from os import name
from django.db import models

# from account.models import (
#     Faculty,
# )



SEMESTER = (
    ('One', '1'),
    ('Two', '2'),
    ('Three', '3'),
    ('Four', '4'),
    ('Five', '5'),
    ('Six', '6'),
    ('Seven', '7'),
    ('Eight', '8'),
)


DESIGNATION = (
    ('Teaching Assistant', 'TA'),
    ('Instructor', 'Instructor'),
    ('Assistant Professor', 'Asst Prof'),
    ('Associate Professor', 'Assoc Prof'),
    ('Professor', 'Prof'),
    ('Head of Department', 'HOD')
)

# Create your models here.


class EmailRecord(models.Model) :
    # serial_no = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    enrollment_no = models.CharField(max_length=15, null=False)
    email_id = models.EmailField(max_length=50, null=False)
    semester = models.CharField(max_length=50, null=False, choices=SEMESTER)

    def __str__(self) :
        return 'Record <' + self.enrollment_no + '>'



class Department(models.Model) :
    name = models.CharField(max_length=50, null=False)
    code = models.CharField(max_length=50, null=False)

    def __str__(self) :
        return self.code

class StaffRecord(models.Model) :
    
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=50, null=False)

    # department = models.CharField(max_length=50, null=False)
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    
    designation = models.CharField(max_length=255, null=False, choices=DESIGNATION)

    def __str__(self) :
        return 'Record <' + self.email + '>'


class Course(models.Model) :
    
    course_name = models.CharField(max_length=255, null=False)
    course_code = models.CharField(max_length=255, null=False)

    semester = models.CharField(max_length=50, null=False, choices=SEMESTER)
    department = models.CharField(max_length=50, null=False)


    # check on this
    teacher = models.ForeignKey('account.Faculty', null=True, on_delete=models.SET_NULL)
    # 'account.Faculty' is string model reference for account.models.Faculty


    def __str__(self) :
        return self.course_name