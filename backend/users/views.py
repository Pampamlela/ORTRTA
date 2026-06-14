from django.shortcuts import render
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from equipment.serializers import CameraSerializer, LensSerializer
from rolls.serializers import RollSerializer, UrlPhotoSerializer
from .serializers import UserSerializer
from rest_framework import generics, status
from .serializers import SignupSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenSerializer
from rolls.models import Roll, UrlPhoto
from equipment.models import Camera, Lens
import logging

logger = logging.getLogger('ortrta')

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Utilisateur"],
        summary="Récupérer son profil",
        description="Retourne les informations du compte de l'utilisateur·ice connecté·e.",
        responses={
            200: UserSerializer,
            401: OpenApiResponse(description="Non authentifié·e"),
        }
    )

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    @extend_schema(
        tags=["Utilisateur"],
        summary="Supprimer son compte",
        description="Supprime définitivement le compte de l'utilisateur·ice connecté·e.",
        responses={
            204: OpenApiResponse(description="Compte supprimé avec succès"),
            401: OpenApiResponse(description="Non authentifié·e"),
        }
    )
    
    def delete(self, request):
        username = request.user.username
        request.user.delete()
        logger.warning("Utilisateur·ice supprimé·e : %s", username)
        return Response({"message": "Utilisateur·ice supprimé·e."}, status=204)

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Authentification"],
        summary="Créer un compte",
        description="Crée un nouveau compte utilisateur·ice et retourne le tokens JWT ainsi que les informations du profil.",
        responses={
            201: OpenApiResponse(
                description="Compte créé avec succès.",
                examples=[
                    OpenApiExample(
                        name="Réponse succès",
                        value={
                            "user": {
                                "id": 1,
                                "username": "john_doe",
                                "email": "john.doe@example.com"
                            },
                            "refresh": "eyJ...",
                            "access": "eyJ..."
                        }
                    )
                ]
            ),
            400: OpenApiResponse(description="Données invalides (champ manquant, email déjà utilisé, etc.)."),
        }
    )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        logger.info("Nouvelle inscription : %s", user.username)

        return Response({
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED) 

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Utilisateur"],
        summary="Changer son mot de passe",
        description="Permet à l'utilisateur·ice connecté·e de changer son mot de passe. Le nouveau mot de passe doit respecter les règles de validation définies dans Django.",
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "password": {
                        "type": "string",
                        "example": "NouveauMotDePasse123!"
                    },
                },
                "required": ["password"]
            }
        },
        responses={
            200: OpenApiResponse(description="Mot de passe mis à jour avec succès."),
            400: OpenApiResponse(description="Mot de passe invalide (ne respecte pas les règles de validation)."),
            401: OpenApiResponse(description="Non authentifié·e"),
        }
    )

    def put(self, request):
        user = request.user
        new_password = request.data.get('password')

        try:
            validate_password(new_password)
        except Exception as e:
            logger.warning("Échec de la validation du mot de passe pour %s : %s", user.username, e)
            raise ValidationError({'password': list(e)})
        
        user.set_password(new_password)
        user.save()

        logger.info("Mot de passe mis à jour pour %s", user.username)

        return Response({'message': 'Mot de passe mis à jour.'})
    
    
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

    @extend_schema(
        tags=["Authentification"],
        summary="Se connecter",
        description="Permet à un.e utilisateur·ice de se connecter en fournissant son nom d'utilisateur et son mot de passe. Retourne un token JWT en cas de succès.",
        responses={
            200: OpenApiResponse(description="Connexion réussie, tokens retournés."),
            401: OpenApiResponse(description="Nom d'utilisateur ou mot de passe incorrect."),
        }
    )

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            logger.info("Connexion réussie pour %s", request.data.get('username'))
            return response
        except Exception as e:
            logger.warning("Échec de connexion pour %s : %s", request.data.get('username'), e)
            raise 


class ExportUserDataView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Utilisateur"],
        summary="Exporter ses données",
        description="Permet à l'utilisateur·ice connecté·e d'exporter toutes les données associées à son compte (appareils, objectifs, pellicules) au format JSON. Utile pour la portabilité des données (RGPD).",
        responses={
             200: OpenApiResponse(
                description="Export des données utilisateur·ice.",
                examples=[
                    OpenApiExample(
                        name="Réponse succès",
                        value={
                            "user": {"id": 1, "username": "exemple", "email": "exemple@mail.com", "date_joined": "2024-01-01"},
                            "cameras": [],
                            "lenses": [],
                            "rolls": [],
                            "photos": [],
                        }
                    )
                ]
            ),
            401: OpenApiResponse(description="Non authentifié·e."),
        }
    )


    def get(self, request):
        user = request.user

        cameras = Camera.objects.filter(user=user)
        lenses = Lens.objects.filter(user=user)
        rolls = Roll.objects.filter(user=user)
        photos = UrlPhoto.objects.filter(roll__user=user)

        data = {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "date_joined": user.date_joined,
            },
            "cameras": CameraSerializer(cameras, many=True).data,
            "lenses": LensSerializer(lenses, many=True).data,
            "rolls": RollSerializer(rolls, many=True).data,
            "photos": UrlPhotoSerializer(photos, many=True).data,
        }

        logger.info("Données exportées pour %s - %d caméras, %d lentilles, %d pellicules, %d photos",
            user.username, cameras.count(), lenses.count(), rolls.count(), photos.count()
        )
        return Response(data)
