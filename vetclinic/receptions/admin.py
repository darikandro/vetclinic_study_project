from django.contrib import admin
from receptions.models import WorkingSlot, Booking, MedicalHistory


admin.site.register(WorkingSlot)
admin.site.register(Booking)
admin.site.register(MedicalHistory)
