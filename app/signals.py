from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from app.models import Profile




@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_associate_tables(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
