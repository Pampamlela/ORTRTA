from django.shortcuts import render
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import generics, status
from .serializers import SignupSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenSerializer
from rolls.models import Roll
from equipment.models import Camera, Lens

# Create your views here.

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def delete(self, request):
        request.user.delete()
        return Response({"message": "Utilisateur supprimé."}, status=204)

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

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
            raise ValidationError({'password': list(e)})
        
        user.set_password(new_password)
        user.save()

        return Response({'message': 'Mot de passe mis à jour.'})
    
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

class ExportUserDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        cameras = Camera.objects.filter(user=user)
        lenses = Lens.objects.filter(user=user)
        rolls = Roll.objects.filter(user=user)

        data = {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "cameras": list(cameras),
            "lenses": list(lenses),
            "rolls": list(rolls),
        }

        return Response(data)
