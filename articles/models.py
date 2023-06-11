from django.contrib.auth.models import User
from django.db import models
from accounts.models import Account


class Article(models.Model):
    title = models.CharField(max_length=70, null=False, blank=False)
    body = models.TextField(null=False, blank=False)
    slug = models.SlugField(max_length=70, null=False)
    author = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    postingDate = models.DateTimeField(auto_now_add=True, null=False)
    isEdited = models.BooleanField(default=False, null=False)
    lastEditDate = models.DateTimeField(auto_now=True, null=False)

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Articles'
