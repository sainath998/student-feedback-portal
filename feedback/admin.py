from django.contrib import admin

from .models import (
    Feedback,
    Voting,
)

from .forms import (
    FeedbackSubmitForm,
)

class FeedbackAdmin(admin.ModelAdmin) :
    form = FeedbackSubmitForm

# Register your models here.

# admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Voting)