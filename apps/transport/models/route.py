from django.db import models
from common.models import BaseModel

class Route(BaseModel):
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    stops = models.JSONField(default=list, help_text="List of pickup points/stops")

    def __str__(self):
        return f"{self.origin} to {self.destination}"
