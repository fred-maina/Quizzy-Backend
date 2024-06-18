from django.contrib.auth.models import User
from django.db import models
from api.models import Quiz

class Leaderboard(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    score=models.IntegerField()
    User=models.ForeignKey(User,on_delete=models.CASCADE)
