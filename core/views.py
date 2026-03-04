import uuid
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Organization, ServiceProvider, AvailabilitySlot, Appointment
from .permissions import HasAPIKey


class RegisterOrganizationView(APIView):
    # No API key needed to register
    def post(self, request):
        organization_name = request.data.get("organization_name")
        username = request.data.get("username")
        password = request.data.get("password")

        if not organization_name or not username or not password:
            return Response(
                {"error": "organization_name, username and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Hash the password before saving!
        hashed_password = make_password(password)
        api_key = str(uuid.uuid4())

        Organization.objects.create(
            name=organization_name,
            username=username,
            password=hashed_password,
            api_key=api_key
        )

        return Response({
            "message": "Organization created successfully",
            "api_key": api_key
        }, status=status.HTTP_201_CREATED)


class ProviderCreateView(APIView):
    permission_classes = [HasAPIKey] # Protect this endpoint

    def post(self, request):
        name = request.data.get("name")
        if not name:
             return Response({"error": "Provider name is required"}, status=status.HTTP_400_BAD_REQUEST)

        provider = ServiceProvider.objects.create(
            name=name,
            # Safely use the organization attached via our permission class
            organization=request.organization 
        )

        return Response({"provider_id": provider.id}, status=status.HTTP_201_CREATED)


class AvailableSlotsView(APIView):
    permission_classes = [HasAPIKey] 

    def get(self, request):
        provider_id = request.GET.get("provider_id")
        date = request.GET.get("date")

        if not provider_id or not date:
            return Response({"error": "provider_id and date are required"}, status=status.HTTP_400_BAD_REQUEST)

        slots = AvailabilitySlot.objects.filter(
            provider_id=provider_id,
            date=date,
            is_booked=False
        )

        data = [{"slot_id": slot.id, "time": str(slot.time)} for slot in slots]
        return Response({"slots": data}, status=status.HTTP_200_OK)


class BookAppointmentView(APIView):
    permission_classes = [HasAPIKey]

    def post(self, request):
        slot_id = request.data.get("slot_id")
        customer_name = request.data.get("customer_name")
        customer_email = request.data.get("customer_email")

        if not all([slot_id, customer_name, customer_email]):
            return Response({"error": "slot_id, customer_name, and customer_email are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Start an atomic database transaction
        with transaction.atomic():
            # Lock the row using select_for_update() to prevent race conditions
            # Use get_object_or_404 to handle invalid IDs gracefully
            slot = get_object_or_404(AvailabilitySlot.objects.select_for_update(), id=slot_id)

            if slot.is_booked:
                return Response({"error": "This slot has already been booked."}, status=status.HTTP_409_CONFLICT)

            appointment = Appointment.objects.create(
                slot=slot,
                customer_name=customer_name,
                customer_email=customer_email
            )

            slot.is_booked = True
            slot.save()

        return Response({"message": "Appointment booked successfully", "appointment_id": appointment.id}, status=status.HTTP_201_CREATED)


class AppointmentListView(APIView):
    permission_classes = [HasAPIKey]

    def get(self, request):
        email = request.GET.get("customer_email")
        if not email:
             return Response({"error": "customer_email is required"}, status=status.HTTP_400_BAD_REQUEST)

        appointments = Appointment.objects.filter(customer_email=email)

        data = [{
            "slot_id": appt.slot.id,
            "time": str(appt.slot.time),
            "date": str(appt.slot.date)
        } for appt in appointments]

        return Response({"appointments": data}, status=status.HTTP_200_OK)