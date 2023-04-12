from django.urls import path
from . import views

urlpatterns = [
    path("", views.join_group_chat, name="join_group_chat"),
    path("<str:group_name>/", views.group_inbox, name="group_inbox"),
    path("checkview", views.checkview, name="checkview"),
    path("send", views.send, name="send"),
    path("getMessages/<str:group_name>/", views.getMessages, name="getMessages"),
]
