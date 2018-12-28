from django.db import models


# Create your models here.

class CSECourse(models.Model):
    cse_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)


class CSETerm(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()