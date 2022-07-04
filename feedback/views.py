from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.defaulttags import register

from django.http import HttpResponse

from .decorators import (
    allowed_users,
)

from .forms import (
    FeedbackSubmitForm,
    DraftEditForm,
    # TestForm,
)

from .models import (
    Feedback,
    Voting,
    FacultyVoting,
)

from account.models import (
    Student,
    Faculty,
)

from personal.models import (
    Course,
)


from account.views import (
    isStudent,
    isFaculty,
)

APPNAME = 'feedback'

# Create your views here.


@login_required(login_url='login')
@allowed_users(roles=['student'])
def renderFeedbackSubmit(request) :
    context = {}

    if request.method == 'POST' :
        feedbackSubmitForm = FeedbackSubmitForm(request, request.POST)
        
        if feedbackSubmitForm.is_valid() :
            course = feedbackSubmitForm.cleaned_data['course']
            course_rating = feedbackSubmitForm.cleaned_data['course_rating']
            content = feedbackSubmitForm.cleaned_data['content']


            student = request.user.student

            if 'draft-btn' in request.POST :
                print(f"submitted from draft")

                feedback = Feedback(
                    content=content,
                    course_rating=course_rating,
                    course=course,
                    student=student,
                    is_draft=True,
                )
                feedback.save()

                student.submitted_feedbacks.add(Course.objects.filter(course_name=course).first())
                student.save()

                messages.success(request, "Your feedback is saved as a draft!")

                return redirect('home')

            feedback = Feedback(
                content=content,
                course_rating=course_rating,
                course=course,
                student=student,
                is_draft=False,
            )
            feedback.save()

            # add the course entry in the submitted_feedbacks attribute of this student,
            student.submitted_feedbacks.add(Course.objects.filter(course_name=course).first())
            # submitted_course = Course.objects.filter(course_name=course).first().course_name
            # student.submitted_feedbacks.append(submitted_course)
            student.save()
            # print(f"submitted_feedbacks for {student} are")
            # print(student.submitted_feedbacks.all())


            # after the feedback object is created and added to m2m of the user,
                # for all users in the system, create a VOTING object corresponding to the new feedback,


            for student in Student.objects.all() :
                new_voting = Voting.objects.create(
                    student=student,    # here 'student' is loop variable,
                    feedback=feedback,
                )
                print(f"{student} --> {new_voting}")

            for faculty in Faculty.objects.all() :
                new_voting = FacultyVoting.objects.create(
                    faculty=faculty,    # here 'faculty' is loop variable,
                    feedback=feedback,
                )

                print(f"{faculty} --> {new_voting}")

            messages.success(request, "Your feedback is submitted successfully!")

            print(f"{feedback.student} submitted feedback at {feedback.date_submitted}")

            return redirect('home')

        else :
            messages.error(request, "The feedback form is not valid!")
            print("Invalid feedback submit form")
            return redirect('submit-feedback')
    
    
    else :
        # Voting.objects.all().delete()
        # FacultyVoting.objects.all().delete()
        # Feedback.objects.all().delete()
        # for crs in Course.objects.all() :
        #     crs.student_set.clear()




        feedbackSubmitForm = FeedbackSubmitForm(request)

    context['feedbackSubmitForm'] = feedbackSubmitForm
    return render(request, APPNAME + '/feedbackSubmit.html', context)

@login_required(login_url='login')
@allowed_users(roles=['student'])
def renderFeedbackView(request) :
    context = {}

    student = request.user.student
    print(f"student votings {student.voting_set.all()}")
    # student_feedbacks = Feedback.objects.filter(student=student)
    # context['student_feedbacks'] = student_feedbacks

    # all_feedbacks = Feedback.objects.all()
    # context['all_feedbacks'] = all_feedbacks

    courses = Course.objects.all()
    course_feedbacks = {}
    for course in courses :
        feedbacks = Feedback.objects.filter(course=course, is_draft=False)
        if len(feedbacks) > 0 :
            for feedback in feedbacks :
                stu_fee_voting = Voting.objects.filter(student=student, feedback=feedback)
            course_feedbacks[course.course_name] = feedbacks

    context['course_feedbacks'] = course_feedbacks

    
    return render(request, APPNAME + '/feedbackView.html', context)

@login_required(login_url='login')
@allowed_users(roles=['faculty'])
def renderFacultyFeedbackView(request) :
    context = {}

    faculty = request.user.faculty
    
    faculty_courses = Course.objects.filter(teacher=faculty)

    print(f"faculty_courses = {faculty_courses}")

    course_feedbacks = {}
    for faculty_course in faculty_courses :
        course_name = faculty_course.course_name
        feedbacks = Feedback.objects.filter(course=faculty_course, is_draft=False)

        if len(feedbacks) > 0 :
            course_feedbacks[course_name] = feedbacks
            print(f"{course_name} --> {feedbacks}")

    # for k, v in course_feedbacks.items() :
    #     print(f"{k} = {v}")

    context['course_feedbacks'] = course_feedbacks

    return render(request, APPNAME + '/facultyFeedbackView.html', context)


@login_required(login_url='login')
@allowed_users(roles=['student'])
def renderEditDraftView(request, draft_id) :
    # print(f"draft_id = {draft_id}")
    context = {}

    draft = Feedback.objects.filter(id=draft_id).first()
    context['draft_course'] = draft.course

    if request.method == 'POST' :
        draftEditForm = DraftEditForm(request.POST)

        if draftEditForm.is_valid() :
            draft.course_rating = draftEditForm.cleaned_data['course_rating']
            draft.content = draftEditForm.cleaned_data['content']

            if 'draft-btn' in request.POST :
                draft.save()

                messages.success(request, "Draft is updated")

                return redirect('home')

            else :
                draft.is_draft = False

                draft.save()

                for student in Student.objects.all() :
                    new_voting = Voting.objects.create(
                        student=student,    # here 'student' is loop variable,
                        feedback=draft,
                    )

                for faculty in Faculty.objects.all() :
                    new_voting = FacultyVoting.objects.create(
                        faculty=faculty,    # here 'faculty' is loop variable,
                        feedback=draft,
                    )

                messages.success(request, "Draft is posted as a feedback")

                return redirect('home')
    else :
        print(f"draft.course is {draft.course}")
        draftEditForm = DraftEditForm(initial={
            'course_rating':draft.course_rating,
            'content':draft.content,
        })

    context['draftEditForm'] = draftEditForm

    return render(request, APPNAME + '/editDraft.html', context)



def upvoteFeedback(request, feedback_id) :
    print(f"upvoting feedback for {feedback_id}")

    query_feedback = Feedback.objects.filter(id=feedback_id).first()

    print(f"upvotes {query_feedback.upvotes}, downvotes {query_feedback.downvotes}, votes {query_feedback.votes}")

    query_feedback.upvotes += 1
    query_feedback.votes += 1

    query_feedback.save()

    print(f"upvotes {query_feedback.upvotes}, downvotes {query_feedback.downvotes}, votes {query_feedback.votes}")

    # also make upvotable false for that student and feedback voting,
    if(isStudent(request)) :
        stu_fee_voting = Voting.objects.filter(student=request.user.student, feedback=query_feedback).first()
        stu_fee_voting.upvotable = False
        stu_fee_voting.downvotable = True
        stu_fee_voting.save()

    if(isFaculty(request)) :
        fac_fee_voting = FacultyVoting.objects.filter(faculty=request.user.faculty, feedback=query_feedback).first()
        fac_fee_voting.upvotable = False
        fac_fee_voting.downvotable = True
        fac_fee_voting.save()


    if isStudent(request) :
        return redirect('view-feedback')
    else :
        return redirect('view-feedback-faculty')


def downvoteFeedback(request, feedback_id) :
    print(f"downvoting feedback for {feedback_id}")

    query_feedback = Feedback.objects.filter(id=feedback_id).first()

    print(f"upvotes {query_feedback.upvotes}, downvotes {query_feedback.downvotes}, votes {query_feedback.votes}")

    query_feedback.downvotes += 1
    query_feedback.votes -= 1

    query_feedback.save()

    print(f"upvotes {query_feedback.upvotes}, downvotes {query_feedback.downvotes}, votes {query_feedback.votes}")

    # also make downvotable false for that student and feedback voting,
    if(isStudent(request)) :
        stu_fee_voting = Voting.objects.filter(student=request.user.student, feedback=query_feedback).first()
        stu_fee_voting.upvotable = True
        stu_fee_voting.downvotable = False
        stu_fee_voting.save()

    if(isFaculty(request)) :
        fac_fee_voting = FacultyVoting.objects.filter(faculty=request.user.faculty, feedback=query_feedback).first()
        fac_fee_voting.upvotable = True
        fac_fee_voting.downvotable = False
        fac_fee_voting.save()

    if isStudent(request) :
        return redirect('view-feedback')
    else :
        return redirect('view-feedback-faculty')


# def TestView(request) :
#     context = {}
#     if request.method == 'POST' :
#         pass
#     else :
#         print(f"request is {request}")
#         testForm = TestForm(initial={
#             'name': 'Manvith'
#         })
#         print(f"testForm {testForm}")

#     context['testForm'] = testForm

#     return render(request, APPNAME + '/editDraft.html', context)


def renderError(request) :
    return render(request, APPNAME + '/errorTemplate.html')


@register.filter
def isUpvotable(request, feedback) :
    if(isStudent(request)) :
        student = request.user.student

        return Voting.objects.filter(student=student, feedback=feedback).first().upvotable

    if(isFaculty(request)) :
        faculty = request.user.faculty

        return FacultyVoting.objects.filter(faculty=faculty, feedback=feedback).first().upvotable


@register.filter
def isDownvotable(request, feedback) :
    if(isStudent(request)) :
        student = request.user.student
        
        return Voting.objects.filter(student=student, feedback=feedback).first().downvotable

    if(isFaculty(request)) :
        faculty = request.user.faculty

        return FacultyVoting.objects.filter(faculty=faculty, feedback=feedback).first().downvotable