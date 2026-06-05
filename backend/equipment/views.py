from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Camera, Lens, Mount
from .serializers import CameraSerializer, LensSerializer, MountSerializer
from .permissions import IsOwner
import logging
logger = logging.getLogger('ortrta')

class CameraViewSet(viewsets.ModelViewSet):
    serializer_class = CameraSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = None

    def get_queryset(self):
        return Camera.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        logger.info("Nouvelle caméra '%s' créée par %s", serializer.instance.model, self.request.user)

    def perform_update(self, serializer):
        camera = self.get_object()
        serializer.save()
        logger.info("Mise à jour de la caméra '%s' par %s - ID : %s", camera.model, self.request.user, camera.id)


class LensViewSet(viewsets.ModelViewSet):
    serializer_class = LensSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = None
    
    def get_queryset(self):
        return Lens.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        logger.info("Nouvelle lentille '%s' créée par %s", serializer.instance.model, self.request.user)

    def perform_update(self, serializer):
        lens = self.get_object()
        serializer.save()
        logger.info("Mise à jour de la lentille '%s' par %s - ID : %s", lens.model, self.request.user, lens.id)


class MountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Mount.objects.all()
    serializer_class = MountSerializer