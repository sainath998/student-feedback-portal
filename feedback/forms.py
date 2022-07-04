from django import forms


from .models import (
    Feedback,
    TestModel,
)

from personal.models import (
    Course,
)

class FeedbackSubmitForm(forms.ModelForm) :
    # RATING_CHOICES = (
    #     ('1', '1'),
    #     ('2', '2'),
    #     ('3', '3'),
    #     ('4', '4'),
    #     ('5', '5'),
    # )

    # course_rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)
    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label='Course')

    class Meta :
        model = Feedback
        fields = ['course', 'course_rating', 'content']

    def __init__(self, request, *args, **kwargs) :
        super(FeedbackSubmitForm, self).__init__(*args, **kwargs)
        
        student = request.user.student
        the_queryset = Course.objects.filter(semester=student.semester)
        # print(f"filtered {the_queryset}")
        
        submitted_courses = student.submitted_feedbacks.all()
        print(f"student already submitted feedbacks to {submitted_courses}")
        
        for course in the_queryset :
            if course in submitted_courses :
                the_queryset = the_queryset.exclude(course_name=course.course_name)
                print(f"{course} is there ({course.course_name})")

        print(f"queryset is {the_queryset}")
        
        self.fields['course'].queryset = the_queryset
        # print(self.fields['course'].queryset)


class DraftEditForm(forms.ModelForm) :

    class Meta :
        model = Feedback
        fields = ['course_rating', 'content']



# class TestForm(forms.ModelForm) :
#     class Meta :
#         model = TestModel
#         fields = '__all__'