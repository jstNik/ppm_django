from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DeleteView
from .models import Comment


class DeleteComment(View):

    def post(self, request, *args, **kwargs):
        comment = Comment.objects.get(pk=request.POST.get('pk'))
        if request.user == comment.author or request.user.is_superuser:
            comment.delete()
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect(request.META.get('HTTP_REFERER'))
