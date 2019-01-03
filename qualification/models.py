from django.db import models

# Create your models here.
from enumfields import Enum, EnumField


class Qualification(models.Model):
    src = models.ForeignKey(to="campaigns.CampaignPartyRelation", on_delete=models.CASCADE,
                            related_name="src_qualifications")
    dst = models.ForeignKey(to="campaigns.CampaignPartyRelation", on_delete=models.CASCADE,
                            related_name="dst_qualifications")


class QuestionType(Enum):
    TYPE_TEXT = "text"
    TYPE_NUMBER = "number"


class Question(models.Model):
    body = models.TextField()
    type = EnumField(QuestionType, max_length=1000)
    coeff = models.IntegerField(default=1)

    def is_valid_ans(self, ans):
        if self.type == QuestionType.TYPE_NUMBER:
            print(self.body)
            try:
                if -1 <= int(ans) <= 100:
                    return True
                else:
                    print("sag")
                    return False
            except:  # in case ans is not number
                print(ans)
                return False
        return True

    def __str__(self):
        return self.body


class QualificationForm(models.Model):
    slug = models.SlugField()

    def __str__(self):
        return self.slug


class QuestionQualificationRelation(models.Model):
    form = models.ForeignKey(to=QualificationForm, on_delete=models.CASCADE, related_name="questions")
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE, related_name="forms")
    place = models.IntegerField()
    def __str__(self):
        return str(self.form) + " | " + str(self.question)

class QA(models.Model):
    qualification = models.ForeignKey(to=Qualification, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(to=QuestionQualificationRelation, on_delete=models.CASCADE, related_name="answers")
    answer = models.TextField()

    def __str__(self):
        return str(self.question) + " | " + str(self.answer)