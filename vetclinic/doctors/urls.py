from django.urls import path
from doctors.views import doctors_list, doctor_page


app_name = "doctors"

urlpatterns = [
    path('', doctors_list, name="list"),
    path('<int:id>/', doctor_page, name="doctor_page"),
]