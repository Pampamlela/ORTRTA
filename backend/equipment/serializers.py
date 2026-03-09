from rest_framework import serializers
from .models import Camera, Lens

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = "__all__"
        read_only_fields = ["user"]

class LensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lens
        fields = "__all__"
        read_only_fields = ["user"]

    def validate_cameras(self, value):
        user = self.context["request"].user

        for camera in value:
            if camera.user != user:
                raise serializers.ValidationError(
                    "Vous ne pouvez associer qu'une caméra qui vous appartient."
                )
        return value