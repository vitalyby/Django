import datetime
from django.db import models
from django.utils import timezone


#

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


# Cur_ID,Date,Cur_Abbreviation,Cur_Scale,Cur_Name,Cur_OfficialRate
class Valuta(models.Model):
    Cur_ID = models.IntegerField()
    Date = models.DateTimeField('Date rate')
    Cur_Abbreviation = models.CharField(max_length=3)
    Cur_Scale = models.IntegerField(default=1)
    Cur_Name = models.CharField(max_length=200)
    Cur_OfficialRate = models.IntegerField()

    def __str__(self):
        return self.Cur_Name
