from django.contrib import admin

from redaction.models import Topic, Redactor, Newspaper

admin.site.register(Topic)
admin.site.register(Redactor)
admin.site.register(Newspaper)
