"""
COMMON DOMAIN - BASE MODELS
---------------------------
Contains reusable model components for the entire project.
The BaseModel ensures every table in the database has UUIDs and Timestamps.
"""
import uuid
from django.db import models

class BaseModel(models.Model):
    """
    Abstract base model that uses UUID for its primary key and includes
    timestamp fields for creation and modification tracking.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
