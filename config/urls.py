from django.contrib import admin
from django.urls import path
from core.views import (
    RegisterOrganizationView, 
    ProviderCreateView, 
    AvailableSlotsView, 
    BookAppointmentView, 
    AppointmentListView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterOrganizationView.as_view(), name='register'),
    path('providers/', ProviderCreateView.as_view(), name='providers'),
    path('slots/', AvailableSlotsView.as_view(), name='slots'),
    path('book/', BookAppointmentView.as_view(), name='book'),
    path('appointments/', AppointmentListView.as_view(), name='appointments'),
]