from django.shortcuts import render
from doctors.models import Doctor

def doctors_list(request):
    doctors = Doctor.objects.all()
    return render(request, "doctors/doctors_list.html", {"doctors_list": doctors})

def doctor_page(request, id):
    doctor = Doctor.objects.get(id=id)
    return render(request, "doctors/doctor_page.html", {"doctor": doctor})
