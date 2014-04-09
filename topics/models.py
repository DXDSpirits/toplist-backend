from django.db import models
from fields import rename, fullpath
from django.utils.translation import ugettext_lazy as _


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

    def __unicode__(self):
        return unicode(self.title)


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

    def score(self):
        return self.win_set.filter(draw=0).count() * 3 + self.win_set.filter(draw=1).count() + self.lose_set.filter(
            draw=1).count()

    def vote_times(self):
        return self.win_set.count() + self.lose_set.count()

    class Meta:
        ordering = ['topic', 'rank']
        index_together = (('topic', 'rank'),)

    def __unicode__(self):
        return unicode(self.title)


class Vote(models.Model):
    IS_DRAW = ((0, _('No')),
               (1, _('Yes')))
    candidate1 = models.ForeignKey(Candidate, null=True, blank=True, related_name='win_set')
    candidate2 = models.ForeignKey(Candidate, null=True, blank=True, related_name='lose_set')
    draw = models.IntegerField(blank=True, null=True, default=0, choices=IS_DRAW)
    topic = models.ForeignKey(Topic, blank=True, null=True)
    time_created = models.DateTimeField(db_column='time_created', auto_now_add=True)
