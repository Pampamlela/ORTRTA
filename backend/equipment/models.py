from django.db import models
from django.conf import settings
# Create your models here.

class Camera(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
          on_delete=models.CASCADE, 
          related_name="cameras")
    model = models.CharField(max_length=100)

    mount = models.ForeignKey(
        'Mount',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cameras'
    )

    has_fixed_lens = models.BooleanField(default=False)
    fixed_lens_model = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.model}"
    
class Lens(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, 
        related_name="lenses"
    )

    model = models.CharField(max_length=100)

    cameras = models.ManyToManyField(
        Camera,
        related_name="lenses",
        blank=True
    )

    mount = models.ForeignKey(
        'Mount',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lenses',
    )
    
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.model}"

class Mount(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name