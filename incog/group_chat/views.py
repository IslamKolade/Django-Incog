from django.shortcuts import render, redirect
from .models import Group_Chat, Group_Messages
from django.http import HttpResponse, JsonResponse
# Create your views here.
def join_group_chat(request):
    return render(request, 'join_group_chat.html')


def group_inbox(request, group_name):
    username = request.GET.get('username')
    group_chat = Group_Chat.objects.get(group_name=group_name)
    return render(request, 'group_messages.html', {
        'username': username,
        'group_name':group_name,
        'group_chat': group_chat, 
        })

def send(request):
    message = request.POST['message']
    username= request.POST['username']
    group_chat_id= request.POST['group_chat_id']

    new_message = Group_Messages.objects.create(message=message, user=username, group_name=group_chat_id)
    new_message.save()
    return HttpResponse('Message sent successfully')


def checkview(request):
    group_name = request.POST['group_name']
    username = request.POST['username']

    if Group_Chat.objects.filter(group_name=group_name).exists():
        return redirect('/group_chat/'+group_name+'/?username='+username)
    else: 
        new_group = Group_Chat.objects.create(group_name=group_name)
        new_group.save()
        return redirect('/group_chat/'+group_name+'/?username='+username)

def getMessages(request, group_name):
    group_chat = Group_Chat.objects.get(group_name=group_name)
    messages = Group_Messages.objects.filter(group_name=group_chat.id)
    return JsonResponse({'messages': list(messages.values())})
