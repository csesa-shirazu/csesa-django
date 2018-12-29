from django.db import models


# Create your models here.

class CSECourse(models.Model):
    cse_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    def __str__(self):
        return str(self.title)


class CSECourseGroup(models.Model):
    course = models.ForeignKey(to=CSECourse, on_delete=models.CASCADE)
    group = models.IntegerField(default=1)

    def __str__(self):
        return str(self.course) + " | " + str(self.group)


class CSETerm(models.Model):
    title = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return str(self.title)


class CSECourseGroupTerm(models.Model):
    course_group = models.ForeignKey(to=CSECourseGroup, on_delete=models.CASCADE)
    term = models.ForeignKey(to=CSETerm, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.course_group) + " | " + str(self.term)

