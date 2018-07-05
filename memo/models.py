from django.db import models
from django.utils import timezone


class Memo(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    related_date = models.DateField(null=True)
    
    def __str__(self):
        return self.title
