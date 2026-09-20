from django.db.models.signals import post_save
from django.dispatch import receiver
from UserApp.models import User,User_Details

@receiver(post_save , sender=User)
def create_admin_record(sender ,created , instance , **kwargs):
    if created:
         User_Details.objects.create(
            user = instance 
        )
        