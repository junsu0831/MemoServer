from django.db import models
from django.utils import timezone


class Memo(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="제목")
    text = models.TextField(verbose_name="내용")
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.title
