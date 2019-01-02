from django.contrib import admin

# Register your models here.
from qualification.models import Question, Qualification, QA, QualificationForm, QuestionQualificationRelation

admin.site.register(Question)
admin.site.register(Qualification)
admin.site.register(QualificationForm)
admin.site.register(QuestionQualificationRelation)
admin.site.register(QA)