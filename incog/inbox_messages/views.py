from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NewChatForm, ChatForm
from .models import Chat, Inboxes
from authentication.models import Profile, Block
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
import secrets
import time
import json
from django.contrib import messages
from django.db.models import Q
from datetime import timezone, datetime
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseBadRequest, StreamingHttpResponse
# from django_sse.views import BaseSseView
import os


def get_video_size(file):
    file.seek(0, os.SEEK_END)
    size = file.tell()
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0


@login_required
def new_chat(request, username):
    # If the request method is POST, the user has submitted a chat form
    if request.method == "POST":
        if request.FILES:
            vid_img = request.FILES.get("vid_img")
            to_user_username = request.POST.get("to_user")
            to_user = User.objects.get(username=to_user_username)
            size = get_video_size(vid_img.file)
            if (
                request.user in to_user.profile.users_blocked.all()
                or to_user.profile.blocked_by_users.all()
            ):
                return HttpResponseForbidden()
            # Create a new Chat object with the form data
            chat = Chat.objects.create(
                sender=request.user,
                recipient=to_user,
            )
            # Generate a unique URL for the chat
            chat.url = secrets.token_hex(16)
            # Save the Chat object
            chat.save()
            if request.user == chat.sender:
                senders_token = chat.sender_token
                recipients_token = chat.recipient_token
            else:
                senders_token = chat.recipient_token
                recipients_token = chat.sender_token
            # Create a new Message object with the user's message
            recipient = User.objects.get(username=to_user_username)
            message = Inboxes.objects.create(
                chat=chat,
                sender=request.user,
                vid_img=vid_img,
                recipient=recipient,
                vid_img_size = size,
                sender_token = senders_token,
                recipient_token = recipients_token,
            )
            # Save the Message object
            message.save()
            # Redirect the user to the chat page
            # return redirect("chat", url=chat.url)
            return redirect("show_messages", url=chat.url)
        else:
            message = request.POST.get("message")
            to_user_username = request.POST.get("to_user")
            to_user = User.objects.get(username=to_user_username)
            if (
                request.user in to_user.profile.users_blocked.all()
                or to_user.profile.blocked_by_users.all()
            ):
                return HttpResponseForbidden()
            # Create a new Chat object with the form data
            chat = Chat.objects.create(
                sender=request.user,
                recipient=to_user,
            )
            # Generate a unique URL for the chat
            chat.url = secrets.token_hex(16)
            # Save the Chat object
            chat.save()

            if request.user == chat.sender:
                senders_token = chat.sender_token
                recipients_token = chat.recipient_token
            else:
                senders_token = chat.recipient_token
                recipients_token = chat.sender_token
            # Create a new Message object with the user's message
            recipient = User.objects.get(username=to_user_username)
            message = Inboxes.objects.create(
                chat=chat,
                sender=request.user,
                message=message,
                recipient=recipient,
                sender_token = senders_token,
                recipient_token = recipients_token,
            )
            # Save the Message object
            message.save()
            # Redirect the user to the chat page
            # return redirect("chat", url=chat.url)
            return redirect("show_messages", url=chat.url)
    # If the request method is GET, render the chat form template
    else:
        try:
            to_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponseForbidden("No such user.")
        if request.user in to_user.profile.users_blocked.all() or to_user.profile.blocked_by_users.all() or request.user == to_user:
            return HttpResponseForbidden("You cannot message this user.")
        form = ChatForm()
        return render(request, "new_chat.html", {"form": form})


@login_required
def block_user(request, user_id, url):
    chat = Chat.objects.get(url=url)
    if request.user not in [chat.sender, chat.recipient]:
        # If the user is not a participant, return a 403 Forbidden response
        return HttpResponseForbidden()
    user_to_block = get_object_or_404(User, id=user_id)
    if user_to_block == request.user:
        return HttpResponseForbidden()
    Block.objects.create(blocker=request.user, blocked=user_to_block)
    request.user.profile.users_blocked.add(user_to_block)
    user_to_block.profile.blocked_by_users.add(request.user)
    return redirect("show_messages", url=url)


@login_required
def unblock_user(request, user_id, url):
    chat = Chat.objects.get(url=url)
    if request.user not in [chat.sender, chat.recipient]:
        # If the user is not a participant, return a 403 Forbidden response
        return HttpResponseForbidden()
    user_to_unblock = get_object_or_404(User, id=user_id)
    Block.objects.filter(blocker=request.user, blocked=user_to_unblock).delete()
    request.user.profile.users_blocked.remove(user_to_unblock)
    user_to_unblock.profile.blocked_by_users.remove(request.user)
    return redirect("show_messages", url=url)


@login_required
def leave_conversation(request, url):
    user = request.user
    chat = Chat.objects.get(url=url)
    if user == chat.sender:
        chat.sender_left_chat = True
        chat.save()
        if chat.sender_left_chat and chat.recipient_left_chat:
            chat.delete()
        return redirect("show_sent_chats")
    elif user == chat.recipient:
        chat.recipient_left_chat = True
        chat.save()
        if chat.sender_left_chat and chat.recipient_left_chat:
            chat.delete()
        return redirect("show_received_chats")
    else:
        # If the user is not a participant, return a 403 Forbidden response.
        return HttpResponseForbidden()


@login_required
def report_conversation(request, url):
    user = request.user
    chat = Chat.objects.get(url=url)
    if user == chat.sender:
        chat.sender_left_chat = True
        chat.save()
        messages.success(
            request,
            "Thank you for reporting this conversation. We take reports very seriously and will investigate this conversation to ensure it does not go against our policies. If we find any inappropriate behavior, we will take appropriate action against the offending user. Thank you for helping us keep Stealth Chat safe and respectful.",
        )
        if chat.sender_left_chat and chat.recipient_left_chat:
            chat.delete()
        return redirect("show_sent_chats")
    elif user == chat.recipient:
        chat.recipient_left_chat = True
        chat.save()
        messages.success(
            request,
            "Thank you for reporting this conversation. We take reports very seriously and will investigate this conversation to ensure it does not go against our policies. If we find any inappropriate behavior, we will take appropriate action against the offending user. Thank you for helping us keep Stealth Chat safe and respectful.",
        )
        if chat.sender_left_chat and chat.recipient_left_chat:
            chat.delete()
        return redirect("show_received_chats")
    else:
        # If the user is not a participant, return a 403 Forbidden response.
        return HttpResponseForbidden()


@login_required
def show_sent_chats(request):
    user = request.user
    # Get the current user's chats
    user_chats = Chat.get_chats(request.user)
    for chat in user_chats:
        chat.unread_messages = chat.unread_messages(request.user)


    # Get the total number of unread messages
    sent_total_unread_messages = sum([chat.unread_messages for chat in user_chats if chat.sender == request.user])
    received_total_unread_messages = sum([chat.unread_messages for chat in user_chats if chat.recipient == request.user])

    return render(request, "sent_chats.html", {"chats": user_chats, "user": user, "sent_total_unread_messages": sent_total_unread_messages, "received_total_unread_messages": received_total_unread_messages})


@login_required
def show_received_chats(request):
    user = request.user
    # Get the current user's chats
    user_chats = Chat.get_chats(request.user)
    for chat in user_chats:
        chat.unread_messages = chat.unread_messages(request.user)

    # Get the total number of unread messages
    sent_total_unread_messages = sum([chat.unread_messages for chat in user_chats if chat.sender == request.user])
    received_total_unread_messages = sum([chat.unread_messages for chat in user_chats if chat.recipient == request.user])


    return render(request, "received_chats.html", {"chats": user_chats, "user": user, "sent_total_unread_messages": sent_total_unread_messages, "received_total_unread_messages": received_total_unread_messages})

@login_required
def get_sent_chats(request):
    user = request.user
    # Get the current user's sent chats
    sent_chats = Chat.get_chats(user)
    chat_list = []
    for chat in sent_chats:
        chat_dict = {
            'url': chat.url,
            'recipient': chat.recipient.username,
            'created_at': chat.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'unread_messages': chat.unread_messages(user),
        }
        chat_list.append(chat_dict)
    return JsonResponse(chat_list, safe=False)

@login_required
def get_received_chats(request):
    user = request.user
    # Get the current user's sent chats
    received_chats = Chat.get_chats(user)
    chat_list = []
    for chat in received_chats:
        chat_dict = {
            'url': chat.url,
            'created_at': chat.created_at,
            'unread_messages': chat.unread_messages(user),
        }
        chat_list.append(chat_dict)
    # Get the total number of unread messages
    sent_total_unread_messages = sum([chat.unread_messages for chat in received_chats if chat.sender == request.user])
    received_total_unread_messages = sum([chat.unread_messages for chat in received_chats if chat.recipient == request.user])
    return JsonResponse(chat_list, sent_total_unread_messages, received_total_unread_messages, safe=False)

from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

@login_required
@require_GET
def collect_messages(request, url):
    chat = Chat.objects.get(url=url)
    if request.user not in [chat.sender, chat.recipient]:
        # If the user is not a participant, return a 403 Forbidden response
        return HttpResponseForbidden()

    def event_stream():
        # Use a generator to create an SSE stream
        messages = Inboxes.objects.filter(chat=chat).order_by("-timestamp")
        for message in reversed(messages):
            message_data = {
                "id": message.id,
                "sender_token": message.sender_token,
                "recipient_token": message.recipient_token,
                "message": message.message,
                "vid_img": message.vid_img.url if message.vid_img else None,
                "vid_img_size": message.vid_img_size if message.vid_img else None,

            }
            event = f"data: {json.dumps(message_data)}\n\n"
            yield event

    # Return the SSE stream as an HTTP response
    response = HttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    return response


@login_required
def get_messages(request, url):
     chat = Chat.objects.get(url=url)
     if request.user not in [chat.sender, chat.recipient]:
         # If the user is not a participant, return a 403 Forbidden response
         return HttpResponseForbidden()
     messages = Inboxes.objects.filter(chat=chat).order_by("-timestamp")

     # Construct a list of message data dictionaries
     message_list = []
     for message in reversed(messages):
         message_data = {
             "id": message.id,
             "sender_token": message.sender_token,
             "recipient_token": message.recipient_token,
             "message": message.message,
             "vid_img": message.vid_img.url if message.vid_img else None,
             "vid_img_size": message.vid_img_size if message.vid_img else None,
             "timestamp": message.timestamp,
         }
         message_list.append(message_data)
     # Return the message data as a JSON response
     return JsonResponse(message_list, safe=False)

def stream_messages(request, url):
    # Get the Chat object
    chat = Chat.objects.get(url=url)
    # Check if the current user is a participant in the chat
    if request.user not in [chat.sender, chat.recipient]:
        # If the user is not a participant, return a 403 Forbidden response
        return HttpResponseForbidden()
    def event_stream():
        last_message_id = None
        while True:
            # Get the messages for the chat
            messages = Inboxes.objects.filter(chat=chat).order_by("-timestamp")
            # Only select messages with IDs greater than the last loaded message ID
            if last_message_id is not None:
                messages = messages.filter(id__gt=last_message_id)
            # Create a dictionary to hold the messages
            data = []
            for message in reversed(messages):
                # Add the message data to the dictionary
                data.append({
                    "sender_token": message.sender_token,
                    "recipient_token": message.recipient_token,
                    "message": message.message,
                    "vid_img": message.vid_img.url if message.vid_img else None,
                    "vid_img_size": message.vid_img_size if message.vid_img else None,
                    "timestamp": message.timestamp,
                })
                # Update the last loaded message ID
                last_message_id = message.id
                # Mark the message as read
                # message.is_read_by_recipient = True
                # message.save()
            # Only yield the event if there are new messages
            if data:
                # Create the SSE event
                event = {
                    "event": "message",
                    "data": json.dumps(data, default=str),
                }
                # Yield the event as a string
                yield f"data: {json.dumps(event)}\n\n"
            # Flush the response to send the event immediately
            response.flush()
            # Wait for 1 second before generating the next event
            time.sleep(0.5)

    # Create a StreamingHttpResponse with the event_stream function as the content
    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    # Set the cache control header to prevent caching of the SSE stream
    response["Cache-Control"] = "no-cache"
    return response

@login_required
def show_messages(request, url):
    # Get the Chat object
    chat = Chat.objects.get(url=url)
    # Check if the current user is a participant in the chat
    if request.user not in [chat.sender, chat.recipient]:
        # If the user is not a participant, return a 403 Forbidden response
        return HttpResponseForbidden()
    # Get the messages for the chat
    messages = Inboxes.objects.filter(chat=chat).order_by("timestamp")
    # If the request method is POST, the user has submitted a reply form
    if request.method == "POST":
        if request.FILES:
            # Bind the form data to a form instance
            vid_img = request.FILES.get("vid_img")
            token = request.POST.get("to_user")
            size = get_video_size(vid_img.file)
            if token == chat.sender_token:
                to_user_username = chat.sender
            elif token == chat.recipient_token:
                to_user_username = chat.recipient
            to_user = User.objects.get(username=to_user_username)

            if request.user == chat.sender:
                senders_token = chat.sender_token
                recipients_token = chat.recipient_token
            else:
                senders_token = chat.recipient_token
                recipients_token = chat.sender_token

            if request.user in to_user.profile.users_blocked.all() or to_user.profile.blocked_by_users.all():
                return HttpResponseForbidden()
            # Create a new Message object with the user's reply
            message = Inboxes.objects.create(
                chat=chat,
                sender=request.user,
                vid_img=vid_img,
                recipient=to_user,
                vid_img_size=size,
                sender_token = senders_token,
                recipient_token = recipients_token,
            )
            # Save the Message object
            message.save()
            # Redirect the user back to the chat page
            return redirect("show_messages", url=url)
        else:
            # Bind the form data to a form instance
            message = request.POST.get("message")
            token = request.POST.get("to_user")
            if token == chat.sender_token:
                to_user_username = chat.sender
            elif token == chat.recipient_token:
                to_user_username = chat.recipient

            to_user = User.objects.get(username=to_user_username)

            if request.user == chat.sender:
                senders_token = chat.sender_token
                recipients_token = chat.recipient_token
            else:
                senders_token = chat.recipient_token
                recipients_token = chat.sender_token


            if request.user in to_user.profile.users_blocked.all() or to_user.profile.blocked_by_users.all():
                return HttpResponseForbidden()
            # Create a new Message object with the user's reply
            message = Inboxes.objects.create(
                chat=chat,
                sender=request.user,
                message=message,
                recipient=to_user,
                sender_token = senders_token,
                recipient_token = recipients_token,
            )
            # Save the Message object
            message.save()
            anything = 'anything'
            data = {
            'anything': anything
            }
            return JsonResponse(data)
    # If the request method is GET, render the chat template with the chat's messages and a reply form
    else:
        user = request.user
        chat = get_object_or_404(Chat, url=url)

        # Mark all messages as read
        Inboxes.objects.filter(
            chat=chat, recipient=user, is_read_by_recipient=False
        ).update(is_read_by_recipient=True)
        Inboxes.objects.filter(chat=chat, sender=user, is_read_by_sender=False).update(
            is_read_by_sender=True
        )
        if request.user == chat.sender:
            token = chat.sender_token
        else:
            token = chat.recipient_token
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return stream_messages(request, url)
    context = {
        "chat":chat,
        "token": token,
        "messages": messages,
    }
    return render(request, "messages.html", context)
