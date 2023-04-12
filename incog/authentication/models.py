from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
# from post.models import Post
from django.utils import timezone
from django.db.models.signals import post_save
import uuid
import os
from django.conf import settings
import shutil


phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

# Create your models here.
def user_directory_path(instance, filename):
    # this file will be uploaded to MEDIA_ROOT/profile_picture_(id)/filename
    profile_pic_folder = 'profile_pictures'
    profile_pic_dir = 'profile_picture_{0}'.format(instance.user.profile.id)
    fullpath = os.path.join(settings.MEDIA_ROOT, profile_pic_folder, profile_pic_dir)

    # Remove the entire directory and its contents if it exists
    if os.path.exists(fullpath):
        shutil.rmtree(fullpath)

    # Create the directory again so the new profile picture can be uploaded
    os.makedirs(fullpath)

    return os.path.join(profile_pic_folder, profile_pic_dir, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    message_id = models.UUIDField(default=uuid.uuid4, editable=False)
    facebook_url = models.URLField(max_length=200, null=True, blank=True)
    instagram_username = models.CharField(max_length=200, null=True, blank=True)
    whatsapp_number = models.CharField(validators=[phone_regex], max_length=15, blank=True, null=True)
    twitter_username = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(max_length=200, null=True, blank=True)
    users_blocked = models.ManyToManyField(User, related_name='users_blocked', blank=True)
    blocked_by_users = models.ManyToManyField(User, related_name='blocked_by_users', blank=True)
    created = models.DateField(auto_now_add=True)
   
    # favorites = models.ManyToManyField(Post)
    profile_picture = models.ImageField(
        upload_to=user_directory_path,
        default="avatar/default_avatar.png",
        blank=True,
        null=True,
        verbose_name="Picture",
    )


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

class LoginAttempt(models.Model):
    username = models.CharField(max_length=255, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Block(models.Model):
    blocker = models.ForeignKey(User, related_name='blocker', on_delete=models.CASCADE)
    blocked = models.ForeignKey(User, related_name='blocked', on_delete=models.CASCADE)


