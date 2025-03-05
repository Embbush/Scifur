from django.contrib.auth.models import User
from django.db import models

class Researcher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Lien avec User
    expertise = models.TextField()
    institution = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
