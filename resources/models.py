from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ManyToManyField("users.Profile", related_name="book")


class Publisher(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Detail(models.Model):
    translator = models.ManyToManyField("users.Profile", related_name="detail")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name="detail")
    version = models.CharField(max_length=20)
    book = models.ForeignKey(Book, related_name="details", on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title + " | " + self.version


class Recommendation(models.Model):
    owner = models.ForeignKey('users.Profile', related_name='recommendations', on_delete=models.CASCADE, null=True)
    text = models.TextField()
    book = models.ForeignKey(Detail, related_name='recommendations', on_delete=models.CASCADE)
