from django.contrib import admin

# Register your models here.
from csecourses.models import CSECourse, CSETerm

admin.site.register(CSECourse)
admin.site.register(CSETerm)