from django.shortcuts import render, get_object_or_404
from django.conf import settings
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from .models import Roll, UrlPhoto, RollStatus
from .serializers import RollSerializer, UrlPhotoSerializer
from.permissions import IsOwner, IsRollOwner
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.db.models import Case, When, Value
import qrcode
from io import BytesIO
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Avg, Value
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample, OpenApiTypes
import logging

logger = logging.getLogger('ortrta')

@extend_schema_view(
    list=extend_schema(
        tags=["Pellicules"],
        summary="Lister ses pellicules",
        description="Retourne la liste paginée des pellicules de l'utilisateur·ice connecté·e."
                    "Supporte le filtrage par statut, apparil, objectif, ISO et format, "
                    "la recherche sur le nom du film et la description, et le tri."
    ),
    retrieve=extend_schema(
        tags=["Pellicules"],
        summary="Détails d'une pellicule",
        responses={
            200: RollSerializer,
            404: OpenApiResponse(description="Pellicule non trouvée ou n'appartenant pas à l'utilisateur·ice connecté·e.")
        }
    ),
    create=extend_schema(
        tags=["Pellicules"],
        summary="Créer une pellicule",
        description="Crée une nouvelle pellicule pour l'utilisateur·ice connecté·e."
    ),
    update=extend_schema(
        tags=["Pellicules"],
        summary="Modifier une pellicule",
        description="Met à jour une pellicule. Si la pellicule est au statut 'scannée, "
                    "seuls les champs 'date_scan' et 'description' peuvent être modifiés.",
        responses={
            200: RollSerializer,
            400: OpenApiResponse(description="Modification interdite sur une pellicule scannée. Seuls les champs 'date_scan' et 'description' peuvent être modifiés."),
            404: OpenApiResponse(description="Pellicule non trouvée ou n'appartenant pas à l'utilisateur·ice connecté·e.")
        }
    ),
    partial_update=extend_schema(
        tags=["Pellicules"],
        summary="Modifier partiellement une pellicule",
        description="Met à jour partiellement une pellicule. Si la pellicule est au statut 'scannée, "
                    "seuls les champs 'date_scan' et 'description' peuvent être modifiés.",
        responses={
            200: RollSerializer,
            400: OpenApiResponse(description="Modification interdite sur une pellicule scannée. Seuls les champs 'date_scan' et 'description' peuvent être modifiés."),
            404: OpenApiResponse(description="Pellicule non trouvée ou n'appartenant pas à l'utilisateur·ice connecté·e.")
        }
    ),
    destroy=extend_schema(
        tags=["Pellicules"],
        summary="Supprimer une pellicule",
        description="Supprime une pellicule. Si la pellicule est au statut 'scannée', la suppression est interdite.",
        responses={
            204: OpenApiResponse(description="Pellicule supprimée avec succès."),
            400: OpenApiResponse(description="Suppression interdite sur une pellicule scannée."),
            404: OpenApiResponse(description="Pellicule non trouvée ou n'appartenant pas à l'utilisateur·ice connecté·e.")
        }
    ),
)
class RollViewSet(viewsets.ModelViewSet):
    serializer_class = RollSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = "slug"
    
    def get_queryset(self):
        return (
            Roll.objects
            .filter(user=self.request.user)
            .select_related("camera", "lens", "user") # pour éviter les requêtes supplémentaires lors de la sérialisation
            .prefetch_related("photos") # si bcp de photos, ça peut être lourd, à tester
            .annotate(status_order=Case(
                When(status=RollStatus.IN_PROGRESS, then=Value(1)),
                When(status=RollStatus.FINISHED, then=Value(2)),
                When(status=RollStatus.DEVELOPED, then=Value(3)),
                When(status=RollStatus.SCANNED, then=Value(4)),
                )
            )
        )
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "camera", "lens", "iso", "format"]
    search_fields = ["film_name", "description"]
    ordering_fields = ["date_start", "created_at", "updated_at", "status_order", "camera__model", "film_name"] #camera__model permet un tri alphabétique sur le modèle de l'appareil photo
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        logger.info("Nouvelle pellicule '%s' créée par %s", serializer.instance.film_name, self.request.user)

    @extend_schema(
        tags=["Pellicules"],
        summary="Générer un QR code pour une pellicule",
        description="Retourne une image PNG contenant un QR code qui point vers la page "
                    "de la pellicule sur le frontend. Accessible uniquement par le propriétaire de la pellicule.",
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.BINARY,
                description="Image PNG du QR code.",
            ),
            404: OpenApiResponse(description="Pellicule introuvable ou n'appartenant pas à l'utilisateur·ice connecté·e."),
        }
    )
    # génération des QrCodes pour chaque roll
    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated, IsOwner])
    def qr(self, request, slug=None):
        
        roll = get_object_or_404(self.get_queryset(), slug=slug)

        url = f"{settings.FRONTEND_URL}/rolls/{roll.slug}/"

        img = qrcode.make(url)

        response = HttpResponse(content_type="image/png")
        img.save(response,"PNG")

        logger.debug("QrCode généré pour le pellicule : %s", roll.slug)
        return response
    
    def perform_update(self, serializer):
        roll = self.get_object()
        if roll.status == RollStatus.SCANNED:
            allowed_fields = {"date_scan", "description"}

            # champs envoyés dans la requête
            incoming_fields = set(serializer.validated_data.keys())

            # si un champ interdit est modifié
            if not incoming_fields.issubset(allowed_fields):
                logger.warning("Modification interdite sur le pellicule scannée : %s - Champs modifiés : %s", roll.slug, incoming_fields)
                raise ValidationError(
                    "Cette pellicule est scannée."
                    "Seul les champs 'date_scan' et 'description' peuvent être modifiés."
                )
    
        serializer.save()
        logger.info("Mise à jour du pellicule '%s' par %s - ID : %s", roll.slug, self.request.user, roll.id)

    def perform_destroy(self, instance):
        if instance.status == RollStatus.SCANNED:
            logger.warning("Suppression interdite sur le pellicule scannée : %s - Utilisateur : %s", instance.slug, self.request.user)
            raise ValidationError("Cette pellicule est scannée et ne peut plus être supprimée.") 
        logger.warning("Pellicule supprimée : %s - Utilisateur : %s", instance.slug, self.request.user)
        instance.delete()
        
@extend_schema_view(
    list=extend_schema(
        tags=["Photos"],
        summary="Lister les stockages des photos",
        description="Retourne la liste des stockages (liens URL) des photos appartenant à l'utilisateur·ice connecté·e."
    ),
    retrieve=extend_schema(
        tags=["Photos"],
        summary="Détail d'un stockage de photo",
        responses={
            200: UrlPhotoSerializer,
            404: OpenApiResponse(description="Stockage de photo introuvable ou n'appartenant pas à l'utilisateur·ice connecté·e."),
        }
    ),
    create=extend_schema(
        tags=["Photos"],
        summary="Ajouter un stockage de photo",
        description="Crée un nouveau stockage (lien URL) pour une photo appartenant à une pellicule de l'utilisateur·ice connecté·e.",
    ),
    update=extend_schema(
        tags=["Photos"],
        summary="Modifier un stockage de photo",
    ),
    partial_update=extend_schema(
        tags=["Photos"],
        summary="Modifier partiellement un stockage de photo",
    ),
    destroy=extend_schema(
        tags=["Photos"],
        summary="Supprimer un stockage de photo",
        responses={
            204: OpenApiResponse(description="Stockage de photo supprimé avec succès."),
            404: OpenApiResponse(description="Stockage de photo introuvable ou n'appartenant pas à l'utilisateur·ice connecté·e."),
        }
    ),
)
class UrlPhotoViewSet(viewsets.ModelViewSet):
    serializer_class = UrlPhotoSerializer
    permission_classes = [IsAuthenticated, IsRollOwner]

    def get_queryset(self):
        return (
            UrlPhoto.objects
            .filter(roll__user=self.request.user)
            .select_related("roll")
        )
    

class UserStatsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Statistiques"],
        summary="Statistiques de l'utilisateur·ice",
        description="Retourne des statistiques sur les pellicules de l'utilisateur·ice connecté·e, "
                    "y compris le nombre total de pellicules, le nombre par statut, "
                    "la moyenne des ISO et le nombre par type de film.",
        responses={
            200: OpenApiResponse(
                description="Statistiques calculées avec succès.",
                examples=[
                    OpenApiExample(
                        name="Réponse succès",
                        value={
                            "total_rolls": 12,
                            "in_progress": 3,
                            "finished": 2,
                            "developed": 4,
                            "scanned": 3,
                            "average_iso": 320.5,
                            "by_film_type": [
                                {"film_type": "color", "count": 8},
                                {"film_type": "bw", "count": 4},
                            ]
                        }  
                    )
                ]
            ),
            401: OpenApiResponse(description="Utilisateur non authentifié."),
        }
    )
    def get(self, request):
        rolls = Roll.objects.filter(user=request.user)

        total_rolls = rolls.count()

        stats = {
            "total_rolls": total_rolls,
            "in_progress": rolls.filter(status=RollStatus.IN_PROGRESS).count(),
            "finished": rolls.filter(status=RollStatus.FINISHED).count(),
            "developed": rolls.filter(status=RollStatus.DEVELOPED).count(),
            "scanned": rolls.filter(status=RollStatus.SCANNED).count(),
            "average_iso": rolls.aggregate(Avg("iso"))["iso__avg"],
            "by_film_type": list(
                rolls.values("film_type")
                .annotate(count=Count("id"))
                .order_by("-count")
            )
        }

        return Response(stats)