from django.contrib import admin
from django.urls import path
from core.views import (
    RegisterOrganizationView,
    ProviderCreateView,
    AvailableSlotsView,
    BookAppointmentView,
    AppointmentListView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/register/', RegisterOrganizationView.as_view()),

    path('api/providers/', ProviderCreateView.as_view()),
    path('api/slots/', AvailableSlotsView.as_view()),
    path('api/book/', BookAppointmentView.as_view()),
    path('api/appointments/', AppointmentListView.as_view()),
]