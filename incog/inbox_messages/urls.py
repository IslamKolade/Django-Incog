from django.urls import path
from . import views

urlpatterns = [
    path("received_chats/", views.show_received_chats, name="show_received_chats"),
    path("sent_chats/", views.show_sent_chats, name="show_sent_chats"),
    path("<str:username>/", views.new_chat, name="new_chat"),
    path("<url>/", views.show_messages, name="show_messages"),
    path("get_messages/<url>/", views.get_messages, name="get_messages"),
    path("collect_messages/<url>/", views.collect_messages, name="collect_messages"),
    path("stream_messages/<url>/", views.stream_messages, name="stream_messages"),
    path("leave_conversation/<url>/", views.leave_conversation, name="leave_conversation"),
    path("report_conversation/<url>/", views.report_conversation, name="report_conversation"),
    path("block_user/<user_id>/<url>/", views.block_user, name="block_user"),
    path("unblock_user/<user_id>/<url>/", views.unblock_user, name="unblock_user"),
    path('get_sent_messages/', views.get_sent_chats, name='get_sent_chats'),
    path('get_received_messages/', views.get_received_chats, name='get_received_chats'),
]
