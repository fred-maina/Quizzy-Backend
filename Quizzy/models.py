from django.contrib.auth.models import User
from django.db import models
from api.models import Quiz

class Leaderboard(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['quiz', 'user'], name='unique_quiz_user')
        ]

    def save(self, *args, **kwargs):
        # Check if an entry with the same quiz and user already exists
        existing_entry = Leaderboard.objects.filter(quiz=self.quiz, user=self.user).first()
        if existing_entry:
            # Update the existing entry
            existing_entry.score = self.score
            super(Leaderboard, existing_entry).save(*args, **kwargs)
        else:
            # Create a new entry
            super(Leaderboard, self).save(*args, **kwargs)
