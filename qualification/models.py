from django.db import models

# Create your models here.
from enumfields import Enum, EnumField


class Qualification(models.Model):
    src = models.ForeignKey(to="campaigns.CampaignPartyRelation", on_delete=models.CASCADE, related_name="src_qualifications")
    dst = models.ForeignKey(to="campaigns.CampaignPartyRelation", on_delete=models.CASCADE, related_name="dst_qualifications")

class QuestionType(Enum):
    TYPE_TEXT = "text"
    TYPE_NUMBER = "number"

class Question(models.Model):
    body = models.TextField()
    type = EnumField(QuestionType, max_length = 1000)
    coeff = models.IntegerField(default=1)

class QA(models.Model):
    qualification = models.ForeignKey(to=Qualification, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE, related_name="answers")
    answer = models.TextField()
