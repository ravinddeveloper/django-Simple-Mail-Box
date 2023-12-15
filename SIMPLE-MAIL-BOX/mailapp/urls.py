from django.urls import path,include
from .views import *
urlpatterns = [
    path('',home,name='home'),
    path('dashboard/',dashboard,name='dashboard'),
    path('mail_details/<id>',mail_details,name='mail_details'),
    path('mail_details/<id>/reply',reply.as_view(),name='reply'),
    path('outbox/<id>',outbox,name='outbox'),
    path('send',send_mail.as_view(),name="send"),

    path('verify/',send_verify_link,name='verify'),
    path('verify/<id>',verify_link),
]
