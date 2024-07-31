from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver

# User Profile Model 
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=12)
    country = models.CharField(max_length=155)
    city = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return self.full_name if not self.user else self.user.username

@receiver(post_save, sender=User)
def post_save_receiver(sender,instance, **kwargs):
    try:
        if instance.profile :
            pass
    except:
        user_profile = Profile.objects.create(user=instance)
