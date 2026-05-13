"""
TRANSPORT DOMAIN - VEHICLE MODELS
---------------------------------
This file defines the Vehicle model, representing the physical 
transportation assets (Buses, Cabs, Troskis) in the Waypik system.
"""
from django.db import models
from common.models import BaseModel

class Vehicle(BaseModel):
    class VehicleType(models.TextChoices):
        BUS = "BUS", "Bus"
        SMART_TROSKI = "SMART_TROSKI", "Smart Troski"
        CAB = "CAB", "Cab"

    v_type = models.CharField(
        max_length=20,
        choices=VehicleType.choices,
        default=VehicleType.BUS
    )
    plate_number = models.CharField(max_length=20, unique=True)
    capacity = models.PositiveIntegerField()
    seat_layout = models.JSONField(help_text="Seating layout configuration (e.g., 2-3 or 2-2 styles)")

    def __str__(self):
        return f"{self.plate_number} ({self.get_v_type_display()})"
