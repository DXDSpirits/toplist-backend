from django.db import models
from fields import rename, fullpath

class Topic(models.Model):
    def image_name(self, filename):
        if self.pk is None:
            return 'topic/%s' % rename(filename)
        else:
            return 'topic/%d/%s' % (self.pk, rename(filename))
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to=image_name, blank=True, null=True)
    def picture_fullpath(self):
        return fullpath(self.picture)


class Candidate(models.Model):
    def image_name(self, filename):
        if self.topic is None or self.topic.pk is None:
            return 'topic/%s' % rename(filename)
        else:
            return 'topic/%d/%s' % (self.topic.pk, rename(filename))
    topic = models.ForeignKey(Topic, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    picture = models.ImageField(upload_to=image_name, blank=True, null=True)
    def thumbnail(self):
        return u'<img src="%s" width=200 height=200>' % (self.picture.url) if self.picture else None
    thumbnail.short_description = 'Thumbnail'
    thumbnail.allow_tags = True
    def picture_fullpath(self):
        return fullpath(self.picture)
    
    class Meta:
        ordering = ['topic', 'rank']
        index_together = (('topic', 'rank'),)
