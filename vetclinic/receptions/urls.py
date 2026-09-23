from django.urls import path
from receptions.views import schedule, schedule_create, select_client, confirm_booking


app_name = "receptions"

urlpatterns = [
    path('', schedule, name="schedule"),
    path('create/', schedule_create, name="create"),
    path('select_client/', select_client, name="select_client"),
    path('confirm/', confirm_booking, name="confirm_booking"),
]