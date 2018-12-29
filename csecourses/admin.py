from django.contrib import admin

# Register your models here.
from csecourses.models import CSECourse, CSETerm, CSECourseGroup, CSECourseGroupTerm

admin.site.register(CSECourse)
admin.site.register(CSETerm)
admin.site.register(CSECourseGroup)
admin.site.register(CSECourseGroupTerm)