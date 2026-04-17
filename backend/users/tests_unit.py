from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from users.models import User

User = get_user_model()

class UserModelFieldsTest(TestCase):
    # test les champs du modèle User
    def test_username_field_is_email(self):
        self.assertEqual(User.USERNAME_FIELD, "email")

    # test que le champ email est unique
    def test_email_field_is_unique(self):
        field = User._meta.get_field("email")
        self.assertTrue(field.unique)

    # test que le champ email est obligatoire
    def test_email_field_is_required(self):
        field = User._meta.get_field("email")
        self.assertFalse(field.null)
        self.assertFalse(field.blank)

    # test que created_at est défini automatiquement à la création de l'utilisateur
    def test_created_at_is_auto_now_add(self):
        field = User._meta.get_field("created_at")
        self.assertTrue(field.auto_now_add)

    # test que updated_at est mis à jour à chaque modification de l'utilisateur    
    def test_updated_at_is_auto_now(self):
        field = User._meta.get_field("updated_at")
        self.assertTrue(field.auto_now)

    
class UserModelCreationTest(TestCase):
    # test la création d'instances User

    # test que l'email est bien défini lors de la création d'un utilisateur
    def test_create_user_sets_email(self):
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        self.assertEqual(user.email, "test@example.com")

    # test que le mot de passe est bien haché et vérifiable
    def test_create_user_hashes_password(self):
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        # le mot de passe ne doit pas être stocké en clair
        self.assertNotEqual(user.password, "testpass123")
        self.assertTrue(user.check_password("testpass123"))

    # test que l'utilisateur créé n'est pas un staff par défaut
    def test_create_user_is_not_staff_by_default(self):
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        self.assertFalse(user.is_staff)

    # test que l'utilisateur créé n'est pas un superuser par défaut
    def test_create_user_is_not_superuser_by_default(self):
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        self.assertFalse(user.is_superuser)

    # test que l'utilisateur créé est un staff et un superuser
    def test_create_superuser_is_staff_and_superuser(self):
        admin = User.objects.create_superuser(
            email="admin@example.com",
            username="adminuser",
            password="adminpass123"
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    # test que la création d'un utilisateur avec un email déjà existant lève une erreur d'intégrité
    def test_duplicate_email_raises_error(self):
        from django.db import transaction
        User.objects.create_user(
            email="test@example.com",
            username="testuser1",
            password="testpass123"
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                User.objects.create_user(
                    email="test@example.com", # même email que le premier user
                    username="testuser2",
                    password="testpass456"
                )
    # test que le champ created_at est bien défini à la création de l'utilisateur       
    def test_created_at_is_set_on_creation(self):
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        self.assertIsNotNone(user.created_at)

    # test que la date de dernière connexion est null tant que l'utilisateur ne s'est jamais connecté
    def test_last_login_is_none_by_default(self):
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        # last_login est null tant que l'utilisateur ne s'est jamais connecté
        self.assertIsNone(user.last_login)