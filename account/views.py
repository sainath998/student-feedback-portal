from http.client import HTTPResponse
from django.http import HttpResponse
from random import random, randint
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.template.defaulttags import register
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.forms import (
    UserCreationForm,
)
from django.contrib.auth.decorators import login_required

from .forms import (
    UserRegistrationForm,
    VerificationForm,
    FacultyRegistrationForm,
    StudentProfileForm,
    FacultyProfileForm,
)

from personal.models import (
    EmailRecord,
    StaffRecord,
    Department,
)

from feedback.models import (
    Feedback,
    Voting,
    FacultyVoting,
)

from .models import (
    Student,
    Faculty,
)

APPNAME = 'account'




# Create your views here.

def renderLogin(request) :
    if request.user.is_authenticated :
        return redirect('home')

    context = {}

    if request.method == 'POST' :
        username = request.POST['username']

        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None :
            login(request, user)
            print(request.user.username)
            print(request.user.last_login)
            # print(request.user.enrollment_no)
            print("logged in")
            return redirect('home')
        else :
            messages.error(request, "The username and password combination is incorrect. Please try again.")
            return redirect('login')
    else :
        return render(request, APPNAME + '/login.html', context)

def renderLogout(request) :
    if request.user.is_authenticated :
        logout(request)
    messages.success(request, "You were successfully logged out.")
    return redirect('home')

def renderRegister(request) :
    if request.user.is_authenticated :
        return redirect('home')


    context = {}

    if request.method == 'POST' :
        registerForm = UserRegistrationForm(request.POST)

        if registerForm.is_valid() :
                        
            username = registerForm.cleaned_data['username']
            password1 = registerForm.cleaned_data['password1']
            password2 = registerForm.cleaned_data['password2']
            enrollment_no = registerForm.cleaned_data['enrollment_no']

            emailRecords = EmailRecord.objects.filter(enrollment_no__iexact=enrollment_no)



            # check if the entered enrollment number is registered in our college
            if(len(emailRecords) == 0) :
                messages.error(request, "This enrollment number is not registered in the college")
                return redirect('register')

            print(emailRecords)
            

            # check if a student with the enrollment number is already registered on the platform
            student = Student.objects.filter(enrollment_no__iexact=enrollment_no)
            if(len(student) != 0) :
                messages.error(request, "A student is already registered with this enrollment number on the platform")
                return redirect('register')
            
            print("not yet registered")

            

            otp = randint(100000, 999999)

            otp_email_body = render_to_string('account/otpEmail.html', {'username': username, 'otp': otp})
            recipient_mail = emailRecords.first().email_id
            print(f"Recipient : {recipient_mail}")

            otp_email = EmailMessage(
                'Verification Code',
                otp_email_body,
                settings.EMAIL_HOST_USER,
                [recipient_mail],
            )


            otp_email.send()

            request.session['into_group'] = 'student'
            request.session['otp'] = otp
            request.session['username'] = username
            request.session['password1'] = password1
            request.session['password2'] = password2
            request.session['enrollment_no'] = enrollment_no
            request.session['emailRecord_name'] = emailRecords.first().name
            request.session['emailRecord_semester'] = emailRecords.first().semester
            request.session['emailRecord_email_id'] = emailRecords.first().email_id

            request.session['is_redirected'] = True
            
            messages.info(request, 'A verification code is sent to the email, use that to confirm your registration')
            return redirect('confirm')

        else :
            print(registerForm.errors.as_json())
            pass

    else :
        registerForm = UserRegistrationForm()

    context['registerForm'] = registerForm


    return render(request, APPNAME + '/register.html', context)


def renderFacultyRegister(request) :
    if request.user.is_authenticated :
        return redirect('home')


    context = {}

    if request.method == 'POST' :
        facultyRegisterForm = FacultyRegistrationForm(request.POST)

        if facultyRegisterForm.is_valid() :
            print("facultyRegisterForm is valid")

            # name = facultyRegisterForm.cleaned_data['name']
            # username = facultyRegisterForm.cleaned_data['username']
            email = facultyRegisterForm.cleaned_data['email']
            password1 = facultyRegisterForm.cleaned_data['password1']
            password2 = facultyRegisterForm.cleaned_data['password2']

            staffRecords = StaffRecord.objects.filter(email__iexact=email)

            # check if the entered email is registered in our college
            if(len(staffRecords) == 0) :
                messages.error(request, "This email is not registered in the college")
                return redirect('register-faculty')

            print(staffRecords)

            faculty = Faculty.objects.filter(email__iexact=email)
            if(len(faculty) != 0) :
                messages.error(request, "A faculty is already registered with this email address on the platform")
                return redirect('register-faculty')
            
            print("not yet registered")

            otp = randint(100000, 999999)

            otp_email_body = render_to_string('account/otpEmail.html', {'username': staffRecords.first().name, 'otp': otp})
            recipient_mail = email
            print(f"Recipient : {recipient_mail}")

            otp_email = EmailMessage(
                'Verification Code',
                otp_email_body,
                settings.EMAIL_HOST_USER,
                # ['supser.respus@gmail.com'], # to be changed
                ['iib2019014@iiita.ac.in'],
            )

            otp_email.send()

            request.session['into_group'] = 'faculty'
            request.session['otp'] = otp
            # request.session['name'] = name
            request.session['email'] = email
            # request.session['username'] = username
            request.session['password1'] = password1
            request.session['password2'] = password2
            request.session['staffRecord_name'] = staffRecords.first().name
            request.session['staffRecord_department_name'] = staffRecords.first().department.name
            request.session['staffRecord_designation'] = staffRecords.first().designation

            request.session['is_redirected'] = True
            
            messages.info(request, 'A verification code is sent to the email, use that to confirm your registration')
            return redirect('confirm')

        else :
            print("registration form is invalid")
            messages.error(request, "There was an error registering you. Please try again.")
            return redirect('register-faculty')

    else :
        facultyRegisterForm = FacultyRegistrationForm()

    context['facultyRegisterForm'] = facultyRegisterForm


    return render(request, APPNAME + '/facultyRegister.html', context)



def renderConfirmation(request) :
    if not 'is_redirected' in request.session :
        messages.error(request, 'The page you requested is not accessible')
        return redirect('home')
    
    context = {}

    # if the form is filled and submitted
    if request.method == 'POST' :

        # registerForm = request.session['registerForm']

        verificationForm = VerificationForm(request.POST)

        if verificationForm.is_valid() :
            print("valid")


            actual_otp = request.session['otp']
            post_otp = verificationForm.cleaned_data['otp']

            print(actual_otp, post_otp)


            # verify the otp
            if post_otp == actual_otp :
                print("otp verified")
                # username = request.session['username']
                password1 = request.session['password1']
                password2 = request.session['password2']


                if request.session['into_group'] == 'student' :
                    print("registering as student")

                    username = request.session['username']
                    enrollment_no = request.session['enrollment_no']
                    emailRecord_name = request.session['emailRecord_name']
                    emailRecord_semester = request.session['emailRecord_semester']
                    emailRecord_email_id = request.session['emailRecord_email_id']

                    user = User.objects.create_user(
                        username=username,
                        email=emailRecord_email_id,
                        password=password1,
                    )

                    student = Student(
                        user=user,
                        name=emailRecord_name,
                        enrollment_no=enrollment_no,
                        email_id=emailRecord_email_id,
                        semester=emailRecord_semester,
                        anonymous_id=username
                    )
                    student.save()


                    # for a new user created, allot the votings for the old feedbacks also,
                    for feedback in Feedback.objects.all() :
                        new_voting = Voting.objects.create(
                            student=student,    # here 'student' is loop variable,
                            feedback=feedback,
                        )

                        print(f"{student} --> {new_voting}")

                    recipient = emailRecord_name
                    recipient_mail = emailRecord_email_id
                    
                    user.groups.add(Group.objects.get(name='student'))

                elif request.session['into_group'] == 'faculty' :
                    print("registering as faculty")

                    # name = request.session['name']
                    email = request.session['email']
                    staffRecord_name = request.session['staffRecord_name']
                    staffRecord_department_name = request.session['staffRecord_department_name']
                    staffRecord_designation = request.session['staffRecord_designation']

                    print(f"staffrecord details {staffRecord_name}, {staffRecord_department_name}, {staffRecord_designation}")

                    unique_random_username = email.split('@')[0] + '_' + email.split('@')[1].split('.')[0]

                    user = User.objects.create_user(
                        username=unique_random_username,
                        email=email,
                        password=password1,
                    )

                    # get the department based on the 'staffRecord_department_name',
                    faculty_department = Department.objects.filter(name=staffRecord_department_name).first()

                    faculty = Faculty.objects.create(
                        user=user,
                        name=staffRecord_name,
                        email=email,
                        department=faculty_department,
                        designation=staffRecord_designation,
                        # username=username,
                    )
                    faculty.save()

                    for feedback in Feedback.objects.all() :
                        new_voting = FacultyVoting.objects.create(
                            faculty=faculty,    # here 'faculty' is loop variable,
                            feedback=feedback,
                        )

                        print(f"{faculty} --> {feedback} -> {new_voting}")

                    recipient = staffRecord_name
                    recipient_mail = email

                    user.groups.add(Group.objects.get(name='faculty'))

                # user = authenticate(username=username, password=password1)

                # login(request, user)

                messages.success(request, "You are successfully registered. You can now login")

                success_email_body = render_to_string('account/successEmail.html', {'username': recipient})
                print(f"Recipient : {recipient_mail}")

                success_email = EmailMessage(
                    'Account Registered',
                    success_email_body,
                    settings.EMAIL_HOST_USER,
                    # ['supser.respus@gmail.com'],
                    [recipient_mail],
                )

                success_email.send()

                del request.session['otp']
                del request.session['is_redirected']


                return redirect('login')

            # if otp is not verified, return error message and redirect to registration
            else :
                print("otp not verified")

                del request.session['otp']
                del request.session['is_redirected']

                messages.error(request, "Invalid verification code")
                return redirect('register')

        else :
            del request.session['otp']
            del request.session['is_redirected']
            
            print("not valid")
            messages.error(request, "Invalid otp form")
            return redirect('register')

            
    
    # if the form is just called(rendered)
    else :
        verificationForm = VerificationForm()
        context['verificationForm'] = verificationForm

        return render(request, APPNAME + '/confirmation.html', context)



@login_required(login_url='login')
def renderProfileView(request, user_id) :
    context = {}

    query_user = User.objects.filter(id=user_id).first()
    print(f"query_user is {query_user}")


    if isStudent(request) :
        query_student = request.user.student

        if request.method == 'POST' :
            studentProfileForm = StudentProfileForm(request.POST, instance=request.user)

            if studentProfileForm.is_valid() :
                query_user.username = studentProfileForm.cleaned_data['username']
                query_user.save()

                query_student.anonymous_id = studentProfileForm.cleaned_data['username']
                query_student.save()

                messages.success(request, "Your profile is updated successfully!")

                return redirect('profile', user_id=request.user.id)

            else :
                print(f"errors are {studentProfileForm.errors}")
                
                messages.error(request, "Error updating profile")

                return redirect('profile', user_id=request.user.id)


        else :
            studentProfileForm = StudentProfileForm(initial={
                'username': query_user.username,
            })

        context['studentProfileForm'] = studentProfileForm

    elif isFaculty(request) :
        query_faculty = query_user.faculty

        if request.method == 'POST' :
            facultyProfileForm = FacultyProfileForm(request.POST, instance=query_user)

            if facultyProfileForm.is_valid() :
                query_faculty.name = facultyProfileForm.cleaned_data['name']
                query_faculty.save()

                messages.success(request, "Your profile is updated successfully!")

                return redirect('profile', user_id=query_user.id)

            else :
                print(f"errors are {facultyProfileForm.errors}")
                
                messages.error(request, "Error updating profile")

                return redirect('profile', user_id=query_user.id)

        else :
            facultyProfileForm = FacultyProfileForm(initial={
                'name': query_faculty.name,
            })

        context['facultyProfileForm'] = facultyProfileForm

    return render(request, APPNAME + '/profile.html', context)







# filters

@register.filter
def isStudent(request) :
    if request.user.groups.exists() :
        if request.user.groups.all()[0].name == 'student' :
            return True

    return False

@register.filter
def isFaculty(request) :
    if request.user.groups.exists() :
        if request.user.groups.all()[0].name == 'faculty' :
            return True

    return False 