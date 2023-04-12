from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, Max
import secrets

def user_directory_path(instance, filename):
    #this file will be uploaded to MEDIA_ROOT/user(id)/filename
    return 'inbox_media/user_{0}/{1}'.format(instance.sender.username, filename)


class Chat(models.Model):
    # This field will store the URL for the chat
    url = models.CharField(max_length=255, unique=True)
    # This field will store the sender of the chat
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats_sent")
    # This field will store the recipient of the chat
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats_received")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sender_token = models.CharField(max_length=255, default=None)
    recipient_token = models.CharField(max_length=255, default=None)
    sender_left_chat = models.BooleanField(default=False)
    recipient_left_chat = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.sender.username} and {self.recipient.username}'s chat"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.sender_token = secrets.token_hex(8)
            self.recipient_token = secrets.token_hex(8)
        super().save(*args, **kwargs)


    def unread_messages(self, user):
    # Get the number of unread messages for the user
        return self.inboxes.filter(Q(recipient=user, is_read_by_recipient=False) | Q(sender=user, is_read_by_sender=False)).count()

    
    def get_chats(user):
        chats = Chat.objects.filter(Q(sender=user) | Q(recipient=user)).annotate(
            last_message=Max("inboxes__timestamp")
        ).exclude(
            (Q(sender=user) & Q(sender_left_chat=True)) | (Q(recipient=user) & Q(recipient_left_chat=True))
        ).order_by("-last_message")
        return chats



class Inboxes(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="inboxes")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    sender_token = models.CharField(max_length=255, default=None)
    recipient_token = models.CharField(max_length=255, default=None)
    message = models.TextField(blank=True, null=True,)
    vid_img = models.FileField(upload_to=user_directory_path, blank=True, null=True,)
    vid_img_size = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read_by_sender = models.BooleanField(default=False)
    is_read_by_recipient = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username}'s message in {self.chat}"

