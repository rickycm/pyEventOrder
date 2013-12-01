# coding=utf-8
from django.db import models

# Create your models here.
class Comment(models.Model):
    userid = models.IntegerField(default=0)
    post = models.TextField('留言', blank=False)
    answer = models.TextField('答复', blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        db_table = 'rest_comment'
        ordering = ['-id']
