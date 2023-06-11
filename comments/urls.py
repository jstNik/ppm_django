from django.urls import path

from comments.views import DeleteComment

app_name = 'comments'

urlpatterns = [
    path('delete', DeleteComment.as_view(), name="delete")
]
