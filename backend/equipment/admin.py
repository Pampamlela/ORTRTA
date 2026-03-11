from django.contrib import admin
from .models import Camera, Lens
from .models import Mount
# Register your models here.

@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ("id", "model", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("model", "user__username")

@admin.register(Lens)
class LensAdmin(admin.ModelAdmin):
    list_display = ("id", "model", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("model", "cameras__model", "user__username")

@admin.register(Mount)
class MountAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    