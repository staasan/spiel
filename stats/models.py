from django.db import models
from django.contrib.auth.models import User


class Result(models.Model):
    db_table = 'EndgameResult'
    RESULT_CHOICES = [
        ("win", "Win"),
        ("draw", "Draw"),
        ("loss", "Loss"),
    ]

    user = models.CharField(max_length=50)
    endgame_type = models.CharField(max_length=50)
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.endgame_type} - {self.result} - {self.created_at}"