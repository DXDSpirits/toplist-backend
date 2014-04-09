from django.contrib import admin
from django.db import models
from django.forms import Textarea
from topics.models import Topic, Candidate, Vote


class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 50})},
    }

    fields = ('thumbnail', 'rank', 'title', 'description', 'picture', )
    readonly_fields = ('thumbnail',)


class TopicAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 50})},
    }
    list_display = ['title', 'description']
    inlines = [CandidateInline]


class VoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'candidate1', 'candidate2', 'draw']


class CandidateAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'rank']


admin.site.register(Topic, TopicAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Candidate, CandidateAdmin)
