from django.shortcuts import render

from .models import (
    EmailRecord,
    Course,
)

from account.models import (
    Faculty,
)

from account.views import (
    isStudent,
    isFaculty,
)


from feedback.models import (
    Feedback,
)

# Create your views here.
def renderHome(request) :
    context = {}
    if request.user.is_authenticated :
        # print(request.user.student)
        print(request.user.email)

        if isStudent(request) :
            student = request.user.student
            context['student_feedbacks'] = Feedback.objects.filter(student=student, is_draft=False)
            print(f"{len(context['student_feedbacks'])} feedbacks")
            context['student_drafts'] = Feedback.objects.filter(student=student, is_draft=True)
            print(f"{len(context['student_drafts'])} drafts")

        # if request.user.student :
        #     sem = request.user.student.semester
        #     courses = Course.objects.filter(semester=sem)
        #     print(f"courses : {courses}")

    emailRecords = EmailRecord.objects.all()
    context["emailRecords"] = emailRecords
    return render(request, 'personal/home.html', context)


def renderContact(request) :
    context = {}
    return render(request, 'personal/contact.html', context)


def renderAbout(request) :
    context = {}
    return render(request, 'personal/about.html', context)