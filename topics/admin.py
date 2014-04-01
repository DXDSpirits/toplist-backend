from django.contrib import admin
from django.db import models
from django.forms import Textarea
from topics.models import Topic, Candidate


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


admin.site.register(Topic, TopicAdmin)
# admin.site.register(Candidate)
