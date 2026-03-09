from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.crypto import get_random_string
# Create your models here.

class RollStatus(models.TextChoices):
    IN_PROGRESS = "IN_PROGRESS", "En cours"
    FINISHED = "FINISHED", "Terminée"
    DEVELOPED = "DEVELOPED", "Développée"
    SCANNED = "SCANNED", "Scannée"

class FilmType(models.TextChoices):
    COLOR_NEGATIVE = "COLOR_NEGATIVE", "Négatif couleur"
    BLACK_AND_WHITE = "BLACK_AND_WHITE", "Noir et blanc"
    COLOR_SLIDE = "COLOR_SLIDE", "Diapositive couleur"

class FilmFormat(models.TextChoices):
    FORMAT_35MM_12 = "35MM-12", "35mm-12"
    FORMAT_35MM_24 = "35MM-24", "35mm-24"
    FORMAT_35MM_36 = "35MM-36", "35mm-36"

    FORMAT_MEDIUM_120_04 = "120-04 (6x17)", "120-04 (6x17)"
    FORMAT_MEDIUM_120_06 = "120-06 (6x12)", "120-06 (6x12)"
    FORMAT_MEDIUM_120_08 = "120-08 (6x9)", "120-08 (6x9)"
    FORMAT_MEDIUM_120_09 = "120-09 (6x8)", "120-09 (6x8)"
    FORMAT_MEDIUM_120_10 = "120-10 (6x7)", "120-10 (6x7)"
    FORMAT_MEDIUM_120_12 = "120-12 (6x6)", "120-12 (6x6)"
    FORMAT_MEDIUM_120_16 = "120-16 (645)", "120-16 (645)"

    FORMAT_MEDIUM_220_08 = "220-08 (6x17)", "220-08 (6x17)"
    FORMAT_MEDIUM_220_12 = "220-12 (6x12)", "220-12 (6x12)"
    FORMAT_MEDIUM_220_16 = "220-16 (6x9)", "220-16 (6x9)"
    FORMAT_MEDIUM_220_18 = "220-18 (6x8)", "220-18 (6x8)"
    FORMAT_MEDIUM_220_20 = "220-20 (6x7)", "220-20 (6x7)"
    FORMAT_MEDIUM_220_24 = "220-24 (6x6)", "220-24 (6x6)"
    FORMAT_MEDIUM_220_32 = "220-32 (645)", "220-32 (645)"

    FORMAT_LARGE_4X5 = "LARGE-4x5", "Grand format 4x5"
    FORMAT_LARGE_5X7 = "LARGE-5x7", "Grand format 5x7"
    FORMAT_LARGE_8X10 = "LARGE-8x10", "Grand format 8x10"

    OTHER_110 = "110", "110"
    OTHER_126 = "126", "126"
    OTHER_127 = "127", "127"

class Roll(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
          on_delete=models.CASCADE, 
          related_name="rolls"
    )
    camera = models.ForeignKey(
        "equipment.Camera",
          on_delete=models.CASCADE, 
          related_name="rolls"
    )
    lens = models.ForeignKey(
        "equipment.Lens",
          on_delete=models.SET_NULL, 
          related_name="rolls",
          null=True, 
          blank=True
    )
    film_name = models.CharField(max_length=100)
    film_type = models.CharField(
        max_length=20,
        choices=FilmType.choices,
        default=FilmType.COLOR_NEGATIVE
    )
    iso = models.IntegerField()
    format = models.CharField(
        max_length=20,
        choices=FilmFormat.choices,
        default=FilmFormat.FORMAT_35MM_36
    )
    description = models.TextField(blank=True)
    date_start = models.DateField()
    date_end = models.DateField(null=True, blank=True)
    date_development = models.DateField(null=True, blank=True)
    date_scan = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=RollStatus.choices,
        default=RollStatus.IN_PROGRESS,
        editable=False
    )
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["status"]),
            models.Index(fields=["date_start"]),
        ]

    def update_status(self):
        if self.date_scan:
            self.status = RollStatus.SCANNED
        elif self.date_development:
            self.status = RollStatus.DEVELOPED
        elif self.date_end:
            self.status = RollStatus.FINISHED
        else:
            self.status = RollStatus.IN_PROGRESS

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.film_name)
            random_part = get_random_string(6)
            self.slug = f"{base_slug}-{random_part}"
        self.update_status()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.film_name} ({self.user.username})"


class PhotoProvider(models.TextChoices):
    FLICKR = "FLICKR", "Flickr"
    GOOGLE_PHOTOS = "GOOGLE_PHOTOS", "Google Photos"
    GOOGLE_DRIVE = "GOOGLE_DRIVE", "Google Drive"
    SITE = "SITE", "Site personnel"
    OTHER = "OTHER", "Autre"
    
class UrlPhoto(models.Model):
    roll = models.ForeignKey(
        Roll,
          on_delete=models.CASCADE, 
          related_name="photos"
    )
    url = models.URLField()
    provider = models.CharField(
        max_length=20,
        choices=PhotoProvider.choices,
        default=PhotoProvider.OTHER
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.url}"