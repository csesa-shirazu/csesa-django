from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(max_length=255, null=True, blank=True)
    file = models.FileField(blank=True, null=True)
    # date_posted = models.CharField(max_length=100, default='shd,dvb', editable=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    telegram_id = models.CharField(max_length=100, default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('telegramboard-home')  # kwargs={'pk': self.pk})

# @receiver(post_save, sender=Post)
# def today():
#     import requests
#     from bs4 import BeautifulSoup
#
#     time_url = 'http://www.time.ir'
#     page = requests.get(time_url)
#     page_content = page.content
#
#     soup = BeautifulSoup(page_content, 'html.parser')
#
#     # print(soup)
#     # months = {'فروردین': 1, 'اردیبهشت': 2, 'خرداد': 3, 'تیر': 4, 'مرداد': 5, 'شهریور': 6,
#     #           'مهر': 7, 'آبان': 8, 'آذر': 9, 'دی': 10, 'بهمن': 11, 'اسفند': 12}
#
#     dates = soup.find('span', attrs={'class': "show date"})
#     tarikh = dates.text
