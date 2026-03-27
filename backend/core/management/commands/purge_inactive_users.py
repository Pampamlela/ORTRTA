from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Supprime les utilisateurices après 2 ans d\'inactivité'

    def handle(self, *args, **kwargs):
        limit_date = timezone.now() - timedelta(days=365*2)

        users = User.objects.filter(last_login__lt=limit_date) | User.objects.filter(last_login__isnull=True, date_joined__lt=limit_date)

        count = users.count()
        users.delete()

        self.stdout.write(f"{count} utilisateurices inactifs ont été supprimé.e.s.")

# à lancer en cron tous les mois pour nettoyer les comptes inactifs