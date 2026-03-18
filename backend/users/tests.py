from django.test import TestCase


from django.urls import reverse
from rest_framework.test import APITestCase #gère JWT, simule requêtes HTTP, teste API DRF
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()

class UserAPITestCase(APITestCase):

    # création d'un utilisateur et obtention du token JWT pour les tests
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="TestPassword123!"
        )

        #Login JWT
        response = self.client.post(
            reverse("token_obtain_pair"),
            {
                "email": "testuser@example.com",
                "password": "TestPassword123!"
            },
        )

        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    # test création d'un utilisateur
    def test_create_user(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "NewPassword123!"
        }

        response = self.client.post("/api/register/", data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.last().email, "newuser@example.com")
        self.assertEqual(User.objects.last().username, "newuser")   

    # test accès à un utilisateur sans token JWT
    def test_cannot_access_user_without_token(self):
        self.client.credentials()  # Supprime les credentials pour simuler une requête sans token

        response = self.client.get(f"/api/me/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test accès à un utilisateur avec un token JWT
    def test_access_user_with_token(self):
        response = self.client.get(f"/api/me/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "testuser@example.com") 
        self.assertEqual(response.data["username"], "testuser")

    # test tentative d'accès à un autre utilisateur
    def test_cannot_access_other_user(self):
        other_user = User.objects.create_user(
            username="otheruser",
            email="otheruser@example.com",
            password="OtherPassword123!"
        )
        response = self.client.get(f"/api/me/{other_user.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test tentative de suppression d'un autre utilisateur
    def test_cannot_delete_other_user(self):
        other_user = User.objects.create_user(
            username="otheruser",
            email="otheruser@example.com",
            password="OtherPassword123!"
        )
        response = self.client.delete(f"/api/me/{other_user.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(User.objects.filter(id=other_user.id).exists(), True)

    # test suppression de son propre compte
    def test_delete_own_account(self):
        response = self.client.delete(f"/api/me/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.filter(id=self.user.id).exists(), False)