from django.db import models


# Create your models here.

class CSECourse(models.Model):
    cse_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    def __str__(self):
        return str(self.title)


class CSECourseGroup(models.Model):
    course = models.ForeignKey(to=CSECourse, on_delete=models.CASCADE)
    group = models.IntegerField()

    def __str__(self):
        return str(self.course)


class CSETerm(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()


class CSECourseGroupTerm(models.Model):
    course_group = models.ForeignKey(to=CSECourse, on_delete=models.CASCADE)
    term = models.ForeignKey(to=CSETerm, on_delete=models.PROTECT)
