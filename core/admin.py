from django.contrib import admin
from .models import Organization, ServiceProvider, AvailabilitySlot, Appointment


admin.site.register(Organization)
admin.site.register(ServiceProvider)
admin.site.register(AvailabilitySlot)
admin.site.register(Appointment)