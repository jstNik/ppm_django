from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    email = models.EmailField(blank=False, null=False, unique=True)
    profile_picture = models.ImageField(blank=True, null=True, default=None, upload_to='./pfps')
    bio = models.TextField(blank=True, max_length=1500, null=True)
    birthday = models.DateField(blank=True, null=True, default=None)

    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'Accounts'

    def __str__(self):
        return str(self.username)
