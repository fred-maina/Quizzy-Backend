from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=255)
    def __str__ (self):
        return self.question_text
        

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    def __str__ (self):
        return self.choice_text
    def save(self, *args, **kwargs):
        # Ensure only one choice per question is marked as correct
        if self.is_correct:
            Choice.objects.filter(question=self.question).exclude(pk=self.pk).update(is_correct=False)
        super().save(*args, **kwargs)
class Bank(models.Model):
    name=models.CharField(max_length=390)
    account_no=models.IntegerField()
    pin=models.IntegerField()
    def __str__(self):
        return self.name