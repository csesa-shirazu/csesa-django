from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey("users.Profile", related_name="book", on_delete=models.CASCADE)


class Detail(models.Model):
    translator = models.TextField()
    publisher = models.CharField(max_length=50)
    version = models.CharField(max_length=20)
    book = models.ForeignKey(Book, related_name="details", on_delete=models.CASCADE)


class Recommendation(models.Model):
    user = models.ForeignKey("users.Profile", on_delete=models.CASCADE)
    recommended = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    encountered = models.BooleanField(default=False)
