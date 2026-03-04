from django.db import models


class Organization(models.Model):

    name = models.CharField(max_length=255)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class ServiceProvider(models.Model):

    name = models.CharField(max_length=255)

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class AvailabilitySlot(models.Model):

    provider = models.ForeignKey(
        ServiceProvider,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    time = models.TimeField()

    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.provider} {self.date} {self.time}"


class Appointment(models.Model):

    slot = models.ForeignKey(
        AvailabilitySlot,
        on_delete=models.CASCADE
    )

    customer_name = models.CharField(max_length=255)

    customer_email = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.slot}"