import uuid
from django.db import models

 
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    def __str__(self):
        return str(self.title)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE,related_name="quiz_questions")  # ForeignKey relationship with Quiz
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,default=1,related_name="question_choices")
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

    def save(self, *args, **kwargs):
        '''Ensure that only one choice per question is correct'''
        if self.is_correct:
            Choice.objects.filter(question=self.question).exclude(pk=self.pk).update(is_correct=False)
        super().save(*args, **kwargs)
