from django.shortcuts import render
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

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

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def delete(self, request):
        username = request.user.username
        request.user.delete()
        logger.warning("Utilisateurice supprimée : %s", username)
        return Response({"message": "Utilisateurice supprimée."}, status=204)

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]


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
