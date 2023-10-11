from django.db.models.signals import post_save
from accounts.models import User, UserProfile
from django.dispatch import receiver


@receiver(post_save, sender=User)
def post_save_create_userprofile(sender, instance, **kwargs):
    profile, create = UserProfile.objects.update_or_create(user=instance)
    profile.save()
