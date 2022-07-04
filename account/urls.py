from django.urls import path

from .views import (
    renderLogin,
    renderLogout,
    renderRegister,
    renderProfileView,
    renderConfirmation,
    renderFacultyRegister,
)

urlpatterns = [
    path('register', renderRegister, name='register'),
    path('register-faculty', renderFacultyRegister, name='register-faculty'),
    path('login', renderLogin, name='login'),
    path('logout', renderLogout, name='logout'),
    path('confirm', renderConfirmation, name='confirm'),
    path('profile/<str:user_id>', renderProfileView, name='profile'),
]