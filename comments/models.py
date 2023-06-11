from django.db import models

from accounts.models import Account
from articles.models import Article


class Comment(models.Model):

    author = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    article = models.ForeignKey(Article, null=False, on_delete=models.CASCADE)
    body = models.TextField(max_length=1000, null=False)
    postingDate = models.DateTimeField(auto_now_add=True)
    isEdited = models.BooleanField(default=False)
    lastEditingDate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Comments'

    def __str__(self):
        return str(self.pk)
