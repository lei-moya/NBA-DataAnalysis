from django.urls import path
from .views import table_check, table_del, table_update

urlpatterns = [
    path("check/", table_check),
    path("del/", table_del),
    path("update/", table_update),
]