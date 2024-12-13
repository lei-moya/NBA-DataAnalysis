from django.urls import path
from .views import data_explore

urlpatterns = [
    path("explore/", data_explore),
]
