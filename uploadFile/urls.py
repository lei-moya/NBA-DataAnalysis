from django.urls import path
from .views import upload_file, upload_message, upload_messages

urlpatterns = [
    path("file/", upload_file),
    path("message/", upload_message),
    path("messages/", upload_messages),
]
