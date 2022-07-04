from django.urls import path

from .views import (
    renderHome,
    renderAbout,
    renderContact,
)


urlpatterns = [
    path('', renderHome, name='home'),
    path('about', renderAbout, name='about'),
    path('contact', renderContact, name='contact'),
]