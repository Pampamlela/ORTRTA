from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Camera, Lens, Mount
from .serializers import CameraSerializer, LensSerializer, MountSerializer
from .permissions import IsOwner
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

import logging
logger = logging.getLogger('ortrta')

@extend_schema_view(
    list=extend_schema(
        tags=["Equipement"],
        summary="Lister ses appareils photo",
        description="Retourne la liste des appareils photo appartenant à l'utilisateur·ice connecté·e.",
    ),
    retrieve=extend_schema(
        tags=["Equipement"],
        summary="Détail d'un appareil photo",
        responses={
            200: CameraSerializer,
            404: OpenApiResponse(description="Appareil introuvable ou n'appartenant pas à l'utilisateur·ice connecté·e."),
        }
    ),
    create=extend_schema(
        tags=["Equipement"],
        summary="Ajouter un appareil photo",
        description="Crée un nouvel appareil photo pour l'utilisateur·ice connecté·e.",  
    ),
    update=extend_schema(
        tags=["Equipement"],
        summary="Modifier un appareil photo",
    ),
    partial_update=extend_schema(
        tags=["Equipement"],
        summary="Modifier partiellement un appareil photo",
    ),
    destroy=extend_schema(
        tags=["Equipement"],
        summary="Supprimer un appareil photo",
        responses={
            204: OpenApiResponse(description="Appareil supprimé avec succès."),
            404: OpenApiResponse(description="Appareil introuvable ou n'appartenant pas à l'utilisateur·ice connecté·e."),
        }
    ),
)
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

@extend_schema_view(
    list=extend_schema(
        tags=["Equipement"],
        summary="Lister ses objectifs",
        description="Retourne la liste des objectifs appartenant à l'utilisateur·ice connecté·e.",
    ),
    retrieve=extend_schema(
        tags=["Equipement"],
        summary="Détail d'un objectif",
        responses={
            200: LensSerializer,
            404: OpenApiResponse(description="Objectif introuvable ou n'appartenant pas à l'utilisateur·ice connecté·e."),
        }
    ),
    create=extend_schema(
        tags=["Equipement"],
        summary="Ajouter un objectif",
        description="Crée un nouvel objectif pour l'utilisateur·ice connecté·e.",
    ),
    update=extend_schema(
        tags=["Equipement"],
        summary="Modifier un objectif",
    ),
    partial_update=extend_schema(
        tags=["Equipement"],
        summary="Modifier partiellement un objectif",
    ),
    destroy=extend_schema(
        tags=["Equipement"],
        summary="Supprimer un objectif",
        responses={
            204: OpenApiResponse(description="Objectif supprimé avec succès."),
            404: OpenApiResponse(description="Objectif introuvable ou n'appartenant pas à l'utilisateur·ice connecté·e."),
        }
    ),
)
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

@extend_schema_view(
    list=extend_schema(
        tags=["Equipement"],
        summary="Lister les montures disponibles",
        description="Retourne la liste des montures (mounts) disponibles dans le système. Lecture seule, commun à tous·tes les utilisateur·ices.",
    ),
    retrieve=extend_schema(
        tags=["Equipement"],
        summary="Détail d'une monture",
        responses={
            200: MountSerializer,
            404: OpenApiResponse(description="Monture introuvable."),
        }
    ),
)
class MountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Mount.objects.all()
    serializer_class = MountSerializer