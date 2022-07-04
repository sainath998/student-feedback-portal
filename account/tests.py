from django.test import TestCase

# * green
# ! red
# ? blue

# Create your tests here.


# register with a enrollment_no that is not registered in our college
# register as a faculty with a email that is not registered in our college

# register with duplicate enrollment number
# register with duplicate email id

# verify with wrong otp
# try to access the confirm page from url box
# try to enter the otp again after the registration is failed (due to invalid otp)



# if a user is deleted, the student or the faculty associated with that user will also be deleted

# if the logged in user is a student, then show 'submit feedback', 'view feedback' for the courses of that student's semesters

# if the logged in user is a faculty, the show 'view feedback' for the courses taught by that Faculty

# if the logged in user is neither a student nor a Faculty, then don't show any of the above



#*** for now... when a student is deleted, associated user is also deleted
# if a user is a student, then if the student is deleted,
    # then that user must be removed from the 'student' group,
    # student.user is set to None
    # also the user now cannot see the 'submit feedback' and 'view feedback' options in home page

#*** for now... when a faculty is deleted, associated user is also deleted
# if a user is a faculty, then if the faculty is deleted,
    # then that user must be removed from the 'faculty' group,
    # faculty.user is set to None
    # also the user now cannot see the 'view feedback' option in home page