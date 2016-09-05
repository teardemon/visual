from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models


class notify(models.Model):
    content = models.CharField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return "idc page notify"
