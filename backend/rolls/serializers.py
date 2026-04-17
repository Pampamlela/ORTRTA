from rest_framework import serializers
from .models import PhotoProvider, Roll, UrlPhoto
from equipment.models import Camera, Lens

class UrlPhotoSerializer(serializers.ModelSerializer):
    roll = serializers.PrimaryKeyRelatedField(queryset=Roll.objects.all())

    class Meta:
        model = UrlPhoto
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate_roll(self, roll):
        user = self.context["request"].user
        if roll.user != user:
            raise serializers.ValidationError(
                "You cannot add a photo to a roll that is not yours."
            )
        return roll

    # def validate(self, data):
    #     user = self.context["request"].user
    #     roll = data.get("roll")

    #     if roll.user != user:
    #         raise serializers.ValidationError(
    #             "You cannot add a photo to a roll that is not yours."
    #         )
        
    #     return data

class RollSerializer(serializers.ModelSerializer):
    photos = UrlPhotoSerializer(many=True, required=False)
    user = serializers.ReadOnlyField(source="user.id")
    camera_name = serializers.ReadOnlyField(source="camera.model")
    lens_name = serializers.ReadOnlyField(source="lens.model")
    
    class Meta:
        model = Roll
        fields = "__all__"
        read_only_fields = (
            "user",
            "slug",
            "status",
            "created_at",
            "updated_at",
        )
    
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
    
    def validate_camera(self, camera):
        user = self.context["request"].user

        if camera.user != user:
            raise serializers.ValidationError(
               "You cannot use a camera that is not yours."
            )
        return camera
    
    def validate_lens(self, lens):
        user = self.context["request"].user

        if lens and lens.user != user:
            raise serializers.ValidationError(
               "You cannot use a lens that is not yours."
            )
        return lens

    def validate(self, data):

        camera = data.get("camera")
        lens = data.get("lens")

        date_start = data.get("date_start")
        date_end = data.get("date_end")
        date_development = data.get("date_development")
        date_scan = data.get("date_scan")

        # Cas update (PATCH) → récupérer les anciennes valeurs
        instance = getattr(self, "instance", None)

        if instance:
            date_start = date_start or instance.date_start
            date_end = date_end or instance.date_end
            date_development = date_development or instance.date_development
            date_scan = date_scan or instance.date_scan
        
        # règles chronologiques
        if date_end and date_end < date_start:
            raise serializers.ValidationError(
                "The end date cannot be before the start date."
            )
        
        if date_development and date_end and date_development < date_end:
            raise serializers.ValidationError(
                "The development date cannot be before the end date."
            )

        if date_scan and date_development and date_scan < date_development:
            raise serializers.ValidationError(
                "The scan date cannot be before the development date."
            )

        # règles de compatibilité matériel
        if camera and lens and camera.mount != lens.mount:
            raise serializers.ValidationError(
                "This lens is not compatible with this camera mount."
            )
        
        return data
    
    def validate_provider(self, value):
        if value not in dict(PhotoProvider.choices):
            raise serializers.ValidationError("Invalid provider.")
        return value
    
    def update(self, instance, validated_data):
        photos_data = validated_data.pop("photos", [])

        instance = super().update(instance, validated_data)

        # supprimer anciens liens
        instance.photos.all().delete()

        # créer les nouveaux liens
        for photo_data in photos_data:
            if photo_data.get("url"): # ignore les champs vides
                UrlPhoto.objects.create(
                    roll=instance,
                    **photo_data
                )
        return instance