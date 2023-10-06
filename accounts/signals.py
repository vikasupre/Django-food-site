from django.db.models.signals import post_save
from accounts.models import User, UserProfile
from django.dispatch import receiver

@receiver(post_save,sender=User)
def post_save_create_userprofile(sender,instance,created,**kwargs):
    # UserProfile.objects.create(user=instance)
    if created:
        print('new user created')
    else:
        print('failed to create new user')
