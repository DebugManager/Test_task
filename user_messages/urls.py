from django.urls import path
from . import views

urlpatterns = [
    path('send_message/', views.SendMessage.as_view()),
    path('message_by_sender/', views.MessageBySender.as_view()),
    path('message_by_receiver/', views.MessageByReceiver.as_view()),
    path('get_user/', views.GetUser.as_view()),
    path('get_web_hook/', views.GetWebHook.as_view()),
]
