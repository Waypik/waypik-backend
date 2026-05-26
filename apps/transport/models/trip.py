from django.db import models
from common.models import BaseModel

class Trip(BaseModel):
    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Scheduled"
        ONGOING = "ONGOING", "Ongoing"
        COMPLETED = "COMPLETED", "Completed"

    vehicle = models.ForeignKey('transport.Vehicle', on_delete=models.CASCADE, related_name="trips")
    route = models.ForeignKey('transport.Route', on_delete=models.CASCADE, related_name="trips")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED
    )
    
    # Tracking Fields
    current_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_long = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    stops_remaining = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Trip {self.id}: {self.route} at {self.departure_time}"
