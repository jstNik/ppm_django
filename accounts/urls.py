from django.urls import path
from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('login', AccountLoginView.as_view(), name='login'),
    path('signup', AccountSignupView.as_view(), name='signup'),
    path('logout', AccountLogoutView.as_view(), name='logout'),
    path('your-profile', AccountProfileView.as_view(), name='your_profile'),
    path('profile/<str:username>', AccountProfileView.as_view(), name='profile'),
    path('edit', AccountEditView.as_view(), name='edit_your_profile'),
    path('edit/<str:username>', AccountEditView.as_view(), name='edit'),
    path('change-password', AccountChangePassword.as_view(), name='change_password'),
    path('delete', AccountDeleteView.as_view(), name='delete_your_profile'),
    path('delete/<str:username>', AccountDeleteView.as_view(), name='delete'),
    path('deletion-confirmed', AccountDeletionConfirmedView.as_view(), name='deletion-confirmed')
]
