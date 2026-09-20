from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Admin

@receiver(post_save , sender=User)
def create_admin_record(sender ,created , instance , **kwargs):
    if created and instance.is_superuser:
         Admin.objects.create(
            Admin_Id =f"ADM{instance.id}",
            Admin_Name = instance.username,
            Email = instance.email,
            Password = instance.password,
            Contact = 0
        )
        