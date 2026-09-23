import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserSecureID(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='secure_id')
    secure_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Secure id for user: {self.user.username}"


@receiver(post_save, sender=User)
def create_user_secure_id(sender, instance, created, **kwargs):
    if created:
        UserSecureID.objects.create(user=instance)
