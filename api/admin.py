from django.contrib import admin
from api.models import Candidate, Interview, Job

# Register your models here.
admin.site.register(Candidate)
admin.site.register(Interview)
admin.site.register(Job)

