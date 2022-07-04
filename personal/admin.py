from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    EmailRecord,
    Department,
    StaffRecord,
    Course,
)

from .forms import (
    CourseForm,
)


class EmailRecordAdmin(admin.ModelAdmin) :
    list_display = ('enrollment_no', 'email_id')

    search_fields = ('enrollment_no', 'email_id')

    ordering = ('enrollment_no', 'email_id')

    filter_horizontal				= ()
    list_filter                     = ()
    fieldsets                       = ()

class DepartmentAdmin(admin.ModelAdmin) :
    list_display = ('name', 'code')

    search_fields = ('name', 'code')

    ordering = ('name', 'code')

    filter_horizontal				= ()
    list_filter                     = ()
    fieldsets                       = ()

class StaffRecordAdmin(admin.ModelAdmin) :
    list_display = ('name', 'email', 'designation', 'department')

    search_fields = ('name', 'email', 'designation', 'department')

    ordering = ('name', 'email', 'designation', 'department')

    filter_horizontal				= ()
    list_filter                     = ()
    fieldsets                       = ()


class CourseAdmin(admin.ModelAdmin) :
    form = CourseForm
    
    list_display = ('course_code', 'course_name', 'teacher', 'semester', 'department')

    search_fields = ('course_code', 'course_name', 'semester', 'department')

    ordering = ('course_code', 'course_name', 'semester', 'department')

    filter_horizontal				= ()
    list_filter                     = ()
    fieldsets                       = ()

# Register your models here.

admin.site.register(EmailRecord, EmailRecordAdmin)

admin.site.register(Department, DepartmentAdmin)

admin.site.register(StaffRecord, StaffRecordAdmin)

admin.site.register(Course, CourseAdmin)