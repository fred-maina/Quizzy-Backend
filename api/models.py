from django.db import models
import random
import string
from django.contrib.auth.models import User  # Import Django's User model
def generate_unique_alphanumeric_code(length=6):
    '''A function that generates a unique code that will be displayed back to the user.'''
    while True:
        code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
        if not Quiz.objects.filter(code=code).exists():
            return code


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=6, default=generate_unique_alphanumeric_code, editable=False, unique=True)   
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Added ForeignKey to User

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
