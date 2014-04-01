from django.db import models
from fields import rename

class Topic(models.Model):
    def image_name(self, filename):
        return 'topic/' + rename(filename)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to=image_name, blank=True, null=True)


class Candidate(models.Model):
    def image_name(self, filename):
        return 'topic/' + rename(filename)
    topic = models.ForeignKey(Topic, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    picture = models.ImageField(upload_to=image_name, blank=True, null=True)
    def thumbnail(self):
        return u'<img src="%s" width=200 height=200>' % (self.picture.url) if self.picture else None
    thumbnail.short_description = 'Thumbnail'
    thumbnail.allow_tags = True
    
    class Meta:
        ordering = ['topic', 'rank']
        index_together = (('topic', 'rank'),)
