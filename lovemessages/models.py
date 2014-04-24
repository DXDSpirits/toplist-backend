from django.db import models

class Message(models.Model):
    site = models.IntegerField(blank=True, null=True, db_index=True)
    content = models.TextField(default='', blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-time_created']
