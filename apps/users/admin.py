from django.contrib import admin
# import the User model from the models module
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("phone", "email", "role", "is_active", "is_staff", "created_at")
    list_filter = ("role", "is_active")
    search_fields = ("phone", "email", "role")
