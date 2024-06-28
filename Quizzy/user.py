from . import models

def save_performance(quiz,score,user):
    
    models.Leaderboard.objects.create(quiz=quiz,score=score,user=user)