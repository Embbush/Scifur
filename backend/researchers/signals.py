from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Researcher

@receiver(post_save, sender=User)
def create_researcher(sender, instance, created, **kwargs):
    if created:
        Researcher.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_researcher(sender, instance, **kwargs):
    instance.researcher.save()
