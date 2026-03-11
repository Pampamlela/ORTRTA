from rest_framework import serializers
from .models import Camera, Lens, Mount

class CameraSerializer(serializers.ModelSerializer):

    lenses = serializers.SerializerMethodField()
    mount_name = serializers.ReadOnlyField(source="mount.name")

    class Meta:
        model = Camera
        fields = "__all__"
        read_only_fields = ["user"]
    
    def get_lenses(self, obj):
        return [
            {"id": lens.id, "model": lens.model}
            for lens in obj.lenses.all()
        ]

class LensSerializer(serializers.ModelSerializer):

    cameras = serializers.SerializerMethodField()
    cameras_ids = serializers.PrimaryKeyRelatedField(
        queryset=Camera.objects.all(),
        many=True,
        write_only=True,
        required=False
    )
    mount_name = serializers.ReadOnlyField(source="mount.name")

    class Meta:
        model = Lens
        fields = "__all__"
        read_only_fields = ["user"]

    def get_cameras(self, obj):
        return [
            {"id": camera.id, "model": camera.model}
            for camera in obj.cameras.all()
        ]

    def validate_cameras_ids(self, value):
        user = self.context["request"].user

        for camera in value:
            if camera.user != user:
                raise serializers.ValidationError(
                    "Vous ne pouvez associer qu'une caméra qui vous appartient."
                )
        return value
    
    def create(self, validated_data):
        cameras = validated_data.pop("cameras_ids", [])
        lens = super().create(validated_data)

        if cameras:
            lens.cameras.set(cameras)
        return lens
    
    def update(self, instance, validated_data):
        cameras = validated_data.pop("cameras_ids", None)
        lens = super().update(instance, validated_data)

        if cameras is not None:
            lens.cameras.set(cameras)
        return lens

class MountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mount
        fields = "__all__"